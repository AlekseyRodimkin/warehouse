from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import PlaceItem, History


@receiver(pre_save, sender=PlaceItem)
def capture_old_place(instance, **kwargs):
    """Сигнал для сохранения старого места для создания записи о перемещении в истории"""
    if not instance.pk:
        instance._old_place = None
        return

    try:
        old_instance = PlaceItem.objects.only("place").get(pk=instance.pk)
        instance._old_place = old_instance.place
    except PlaceItem.DoesNotExist:
        instance._old_place = None


@receiver(post_save, sender=PlaceItem)
def log_place_change(instance, created, **kwargs):
    """Сигнал для создания записи в History, только если место действительно изменилось."""
    if created:
        return

    old_place = getattr(instance, "_old_place", None)
    new_place = instance.place

    if old_place == new_place or old_place is None:
        return

    user = getattr(instance, "_current_user", None)

    History.objects.create(
        user=user,
        item=instance.item,
        old_place=old_place,
        new_place=new_place,
    )
