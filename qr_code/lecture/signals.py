import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from qr_code.students.models import Student
from qr_code.doctors.models import Doctor
from qr_code.users.models import User
from .models import AttendanceRequest, QRCode
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.conf import settings

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AttendanceRequest)
def create_qr_code(sender, instance, created, **kwargs):
    if created:
        img = qrcode.make(str(instance.id))
        type(img)  # qrcode.image.pil.PilImage
        img.save("{1}/media/{0}.png".format(instance.id, settings.APPS_DIR))
        QRCode.objects.create(
            attendance_request=instance,
            qrcode="/{0}.png".format(instance.id),
            ).save()

# @receiver(post_save, sender=AttendanceRequest)
# def save_qr_code(sender, instance, **kwargs):
#     instance.qr_codes.save()
#     logger.info(f"{instance}'s qr_code created")
