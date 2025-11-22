from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
    """
    Модель товара

    pk: int
    weight: int: 1 < weight < 100.000.000
    item_code: str: len(item_code) <= 100
    description: str: len(description) <= 500
    created_at: datetime: 2000-01-02 10:30:45.123456+00:00
    """

    weight = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100000000)],
    )
    item_code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Приводит код товара к верхнему регистру перед сохранением"""
        if self.item_code:
            self.item_code = self.item_code.strip().upper()
        super().save(*args, **kwargs)

    @property
    def description_short(self) -> str:
        return (
            self.description
            if len(self.description) < 48
            else self.description[:48] + "..."
        )

    class Meta:
        ordering = ["item_code"]

    #     indexes = [
    #         models.Index(fields=['item_code', 'created_at']),
    #     ]
    #     # verbose_name = "Товар"
    #     # verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.item_code}"


class Place(models.Model):
    """
    Модель места

    pk: int
    title: str: len(address) <= 100
    description: str: len(description) <= 500
    created_at: datetime: 2000-01-02 10:30:45.123456+00:00
    zone: Zone
    """

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    zone = models.ForeignKey(
        "Zone",
        on_delete=models.CASCADE,
        related_name="places",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        """Приводит код места к верхнему регистру перед сохранением"""
        if self.title:
            self.title = self.title.strip().upper()
        super().save(*args, **kwargs)

    @property
    def description_short(self) -> str:
        return (
            self.description
            if len(self.description) < 48
            else self.description[:48] + "..."
        )

    @property
    def full_address(self) -> str:
        """
        Возвращает полный адрес
        Если нет родителей: "title"
        Если есть zone: "zone.title/title"
        Если есть stock: "stock.title/zone.title/title"
        """
        parts = [self.title]
        if self.zone:
            parts.insert(0, self.zone.title)
            if self.zone.stock:
                parts.insert(0, self.zone.stock.title)
        return "/".join(parts)

    class Meta:
        ordering = ["title"]

    #     indexes = [
    #         models.Index(fields=['title', ]),
    #     ]

    def __str__(self):
        return f"{self.title}"


class PlaceItem(models.Model):
    """
    Промежуточная таблица: товар на конкретном адресе

    pk: int
    place: Place
    item: Item
    quantity: int
    """

    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="place_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="place_items")
    quantity = models.PositiveIntegerField(default=1)
    STATUSES_CHOICES = [
        ("ok", "ok"),
        ("blk", "blk"),
        ("no", "no"),
        ("new", "new"),
        ("dock", "dock"),
    ]

    STATUS = models.CharField(
        max_length=20,
        choices=STATUSES_CHOICES,
        default="new",
    )

    @property
    def full_address(self) -> str:
        """
        Возвращает полный адрес
        Если нет родителей: "place.title"
        Если есть zone: "place.zone.title/place.title"
        Если есть stock: "place.zone.stock.title/zone.title/place.title"
        """
        parts = [self.place.title]
        if self.place.zone:
            parts.insert(0, self.place.zone.title)
            if self.place.zone.stock:
                parts.insert(0, self.place.zone.stock.title)
        return "/".join(parts)

    class Meta:
        ordering = ["pk"]
        unique_together = (
            "place",
            "item",
        )  # Один товар не может дублироваться в одном месте

    def __str__(self):
        return f"{self.item.item_code} x{self.quantity} @ {self.place.title}"


class Zone(models.Model):
    """
    Модель зоны

    pk: int
    title: str: len(address) <= 100
    description: str: len(description) <= 500
    created_at: datetime: 2000-01-02 10:30:45.123456+00:00
    stock: Stock
    """

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.ForeignKey(
        "Stock",
        on_delete=models.CASCADE,
        related_name="zones",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        """Приводит код зоны к верхнему регистру перед сохранением"""
        if self.title:
            self.title = self.title.strip().upper()
        super().save(*args, **kwargs)

    @property
    def description_short(self) -> str:
        return (
            self.description
            if len(self.description) < 48
            else self.description[:48] + "..."
        )

    @property
    def full_address(self) -> str:
        """
        Возвращает полный адрес
        Если нет родителя: "title"
        Если есть stock: "stock.title/title"
        """
        parts = [self.title]
        if self.stock:
            parts.insert(0, self.stock.title)
        return "/".join(parts)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}"


class Stock(models.Model):
    """
    Модель склада

    pk: int
    title: str: len(address) <= 100
    address: str: len(address) <= 300
    description: str: len(description) <= 500
    created_at: datetime: 2000-01-02 10:30:45.123456+00:00
    """

    title = models.CharField(max_length=100)
    address = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Приводит код склада к верхнему регистру перед сохранением"""
        if self.title:
            self.title = self.title.strip().upper()
        super().save(*args, **kwargs)

    @property
    def description_short(self) -> str:
        return (
            self.description
            if len(self.description) < 48
            else self.description[:48] + "..."
        )

    class Meta:
        ordering = ["pk"]

    #     indexes = [
    #         models.Index(fields=['title', 'address', 'created_at']),
    #     ]

    def __str__(self):
        return f"{self.title}"


class History(models.Model):
    """
    Модель истории переселения

    pk: int
    date: datetime: 2000-01-02 10:30:45.123456+00:00
    user: User
    item: Item
    old_place: str: Place
    new_place: str: Place
    """

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT
    )
    count = models.PositiveIntegerField(default=1)
    old_place = models.ForeignKey(
        Place,
        on_delete=models.PROTECT,
        related_name="history_old_place",
    )

    new_place = models.ForeignKey(
        Place,
        on_delete=models.PROTECT,
        related_name="history_new_place",
    )

    @property
    def full_old_address(self) -> str:
        """
        Возвращает полный старый адрес
        'stock.title/zone.title/place.title'
        """
        return "{stock}/{zone}/{place}".format(
            stock=self.old_place.zone.stock.title,
            zone=self.old_place.zone.title,
            place=self.old_place.title,
        )

    @property
    def full_new_address(self) -> str:
        """
        Возвращает полный новый адрес
        'stock.title/zone.title/place.title'
        """
        return "{stock}/{zone}/{place}".format(
            stock=self.new_place.zone.stock.title,
            zone=self.new_place.zone.title,
            place=self.new_place.title,
        )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"History #{self.pk}"
