from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from qr_code.common.models import TimeStampedUUIDModel

User = get_user_model()


class Doctor(TimeStampedUUIDModel):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        OTHER = "other", _("other")

    user = models.OneToOneField(User, related_name="doctor", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name=_("phone number"), max_length=30, default="+250784123456"
    )
    about_me = models.TextField(
        verbose_name=_("about me"),
        default="say something about yourself",
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.MALE,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("country"), default="EG", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("city"),
        max_length=180,
        default="Ciro",
        blank=False,
        null=False,
    )
    age = models.IntegerField(blank=True, null=True)
    doctor_photo = models.ImageField(
        verbose_name=_("Doctor photo"), default="/doctor_default.png"
    )

    def __str__(self):
        return f"{self.user.username}'s Doctor"

    