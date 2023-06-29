from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from qr_code.common.models import TimeStampedUUIDModel
from qr_code.courses.models import Course, StudentCourses
from qr_code.lecture.models import Lectures, AttendanceRequest
User = get_user_model()


class Student(TimeStampedUUIDModel):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        OTHER = "other", _("other")

    user = models.OneToOneField(User, related_name="student", on_delete=models.CASCADE)
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
    student_id = models.CharField(max_length=255,blank=True,null=True)
    student_photo = models.ImageField(
        verbose_name=_("student photo"), default="/student_default.png"
    )

    def __str__(self):
        return f"{self.user.username}'s student"

    
class StudentAttendance(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        ACCEPTED = "accepted", _("accepted")
        REJECTED = "rejected", _("rejected")

    student = models.ForeignKey(Student, related_name="student_attendance", on_delete=models.CASCADE)
    lecture = models.ForeignKey(
        Lectures, related_name="student_att_lecture", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="student_att_course", on_delete=models.CASCADE
    )
    attendance_request = models.ForeignKey(AttendanceRequest, related_name="student_attendance_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REJECTED)
    week_no = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.student.user.username}'s student"
    
    