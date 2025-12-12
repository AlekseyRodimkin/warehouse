import logging
import os
import shutil

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Inbound

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Inbound)
def delete_inbound_documents(sender, instance, **kwargs):
    """Удаляет папку с именем inbound.inbound_number после удаления Inbound."""
    if not instance.inbound_number:
        return

    inbound_folder = os.path.join(
        settings.MEDIA_ROOT, "inbounds", instance.inbound_number
    )
    if os.path.exists(inbound_folder) and os.path.isdir(inbound_folder):
        try:
            shutil.rmtree(inbound_folder)
            logger.debug(f"Folder {inbound_folder} successfully deleted")
        except Exception as e:
            logger.debug(f"Error deleting folder {inbound_folder}: {e}")
