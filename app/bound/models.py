from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from warehouse.models import Item, Stock


class Inbound(models.Model):
    """
    Модель поставки товаров

    pk: int
    stock: Stock
    created_by: User
    inbound_number: str
    status: str
    planned_date: datetime
    actual_date: datetime
    supplier: User
    updated_at: datetime
    """

    STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("planned", "Запланирован"),
        ("in_progress", "В процессе"),
        ("completed", "Завершен"),
        ("cancelled", "Отменен"),
    ]

    stock = models.ForeignKey(
        Stock, on_delete=models.PROTECT, related_name="inbounds", verbose_name="Склад"
    )

    created_by = models.CharField(max_length=100, verbose_name="Создал")

    inbound_number = models.CharField(
        max_length=50, unique=True, verbose_name="Номер поставки", null=True, blank=True
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft", verbose_name="Статус"
    )

    planned_date = models.DateField(verbose_name="Планируемая дата")

    actual_date = models.DateField(
        null=True, blank=True, verbose_name="Фактическая дата"
    )

    supplier = models.CharField(max_length=200, blank=True, verbose_name="Поставщик")

    description = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Описание"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"
        ordering = ["-created_at"]
        # indexes = [
        #     models.Index(fields=['document_number']),
        #     models.Index(fields=['status', 'planned_date']),
        #     models.Index(fields=['stock', 'created_at']),
        # ]

    def save(self, *args, **kwargs):
        """
        Автогенерация номера поставки
        Пример:
        """
        if not self.inbound_number:
            year = timezone.now().year
            count = Inbound.objects.filter(created_at__year=year).count() + 1
            self.inbound_number = f"INB-{year}-{count:04d}"

        # Устанавливаем фактическую дату при завершении
        if self.status == "completed" and not self.actual_date:
            self.actual_date = timezone.now().date()

        super().save(*args, **kwargs)

    @property
    def description_short(self) -> str:
        if not self.description:
            return ""
        return (
            self.description
            if len(self.description) < 48
            else self.description[:48] + "..."
        )

    @property
    def total_items(self):
        """Общее количество позиций"""
        return self.inbound_items.count()

    @property
    def total_quantity(self):
        """Общее количество товара"""
        return sum(item.total_quantity for item in self.inbound_items.all())

    @property
    def is_completed(self):
        """Приход завершен"""
        return self.status == "completed"

    def __str__(self):
        return f"{self.inbound_number}"


class InboundItem(models.Model):
    """
    Позиция поставки - конкретный товар в поставке

    pk: int
    inbound: Inbound
    total_quantity: int
    created_at: datetime
    item: Item
    """

    inbound = models.ForeignKey(
        Inbound,
        on_delete=models.CASCADE,
        related_name="inbound_items",
        verbose_name="Приход",
    )

    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Товар")

    total_quantity = models.PositiveIntegerField(verbose_name="Количество")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Позиция поставки"
        verbose_name_plural = "Позиции поставки"
        # unique_together = ('inbound', 'item')
        ordering = ["pk"]

    def save(self, *args, **kwargs):
        """Автоматическое обновление статуса"""
        ...
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.item_code} x{self.total_quantity}"
