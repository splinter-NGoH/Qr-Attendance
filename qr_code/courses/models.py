from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

from qr_code.common.models import TimeStampedUUIDModel
# from sett_elkol.ratings.models import Rating

# from .read_time_engine import ArticleReadTimeEngine

User = get_user_model()


class Course(TimeStampedUUIDModel):
    user = models.ManyToManyField(
        User, verbose_name=_("Doctor"), related_name="doctors_assigned"
    )
    title = models.CharField(verbose_name=_("title"), max_length=250)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.CharField(verbose_name=_("description"), max_length=255,unique=True)
    banner_image = models.ImageField(
        verbose_name=_("banner image"), default="/customer_default.jpg"
    )
    session_counts = models.IntegerField(verbose_name=_("session_counts"), default=12)

    def __str__(self):
        return f"{self.slug} Course Code"

    @property
    def list_of_doctors(self):
        doctors = [{"username": doctor.username, "usertype": doctor.user_type} for doctor in self.user.all()]
        return doctors


    def get_doctors_assigned_to_course(self, course):
        return self.doctors_assigned.filter(pkid=course.user.pkid)


class StudentCourses(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Student"), related_name="students_assigned"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course"), related_name="courses_to_students"
    )
    def __str__(self):
        return f"{self.user.username}'s Student"

    class Meta:
        verbose_name = "Course Assigned To Student"
        verbose_name_plural = "Courses Assigned To Students"
        unique_together = ("user", "course")