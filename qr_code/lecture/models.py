from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

from qr_code.common.models import TimeStampedUUIDModel
from qr_code.courses.models import Course

User = get_user_model()




class Lectures(TimeStampedUUIDModel):
    class Types(models.TextChoices):
        SECTION = "section", _("section")
        LECTURE = "lecture", _("lecture")
    title = models.CharField(verbose_name=_("title"), max_length=250)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.TextField(verbose_name=_("description"), max_length=255)
    floor = models.CharField(verbose_name=_("lecture floor"),max_length=20)
    lecture_no = models.IntegerField(verbose_name=_("lecture number"), default=0)
    type = models.CharField(verbose_name=_("Type"), choices=Types.choices, default=Types.SECTION,max_length=20)

    def __str__(self):
        return f"{self.title}"


class AttendanceRequest(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User, related_name="doctor_creating_attendance_request", on_delete=models.CASCADE
    )
    lecture = models.ForeignKey(
        Lectures, related_name="lecture_attendance_request", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="course_attendance_request", on_delete=models.CASCADE
    )
    period = models.IntegerField(default=0)
    week_no = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "AttendanceRequest"
        verbose_name_plural = "AttendanceRequests"

class QRCode(TimeStampedUUIDModel):
    attendance_request = models.ForeignKey(
        AttendanceRequest, related_name="qr_codes", on_delete=models.CASCADE
    )    
    qrcode = models.ImageField(
        verbose_name=_("qrcode image"), default="/faild.jpg"
    )
    def __str__(self):
        return self.attendance_request.lecture.title
