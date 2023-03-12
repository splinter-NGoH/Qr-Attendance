from django.urls import path

from .views import (
    CreateAttendanceRequestAPIView,
    LectureListAPIView,
)

urlpatterns = [
    path("all/", LectureListAPIView.as_view(), name="all-profiles"),
    path("list/", CreateAttendanceRequestAPIView.as_view(), name="list-attendanceforuser"),
    path(
        "create/attendancerequest/", CreateAttendanceRequestAPIView.as_view(), name="create-attendanceforuser"
    ),
   
]
