from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
    """
    Модель товара

    price: float: 0 < price < 100.000.000
    weight: int: 1 < weight < 100.000.000
    total_qty: int: 0 < total_qty < 100.000.000
    item_code: str: len(item_code) <= 100
    description: str: len(description) <= 500
    created_at: datetime: 2000-01-02 10:30:45.123456+00:00
    """
    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100000000)],
    )
    weight = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100000000)],
    )
    total_qty = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(100000000)],
    )
    item_code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["item_code"]
        indexes = [
            models.Index(fields=['item_code', 'created_at']),
        ]
        # verbose_name = "Товар"
        # verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.item_code}"


class Stock(models.Model):
    """
    Модель склада

    """

    # class Meta:
    #     ordering = ["pk"]
    #

    def __str__(self):
        return f"{self.item_code}"
