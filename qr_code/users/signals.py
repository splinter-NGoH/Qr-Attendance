import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from config.settings.base import AUTH_USER_MODEL
from qr_code.students.models import Student
from qr_code.doctors.models import Doctor
from qr_code.users.models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_student_doctor(sender, instance, created, **kwargs):
    if created and instance.user_type == User.UserType.STUDENT:
        Student.objects.create(
            user=instance,
            student_id=instance.student_id,
            gender=instance.gender,
            ).save()
    if created and instance.user_type == User.UserType.DOCTOR:
        Doctor.objects.create(user=instance,
                            gender=instance.gender,
                            ).save()

@receiver(post_save, sender=AUTH_USER_MODEL)
def save_student_doctor(sender, instance, **kwargs):
    # if  instance.user_type == User.UserType.STUDENT:
    #     instance.student.save()
    #     logger.info(f"{instance}'s student created")
    # if  instance.user_type == User.UserType.DOCTOR:
    #     instance.doctor.save()
    #     logger.info(f"{instance}'s doctor created")
    pass