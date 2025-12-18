from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Profile(models.Model):
    """
    Модель профиля

    pk: int
    user: User
    gender: str
    """

    user = models.OneToOneField(User, on_delete=CASCADE)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Profile #{self.user.username}"
