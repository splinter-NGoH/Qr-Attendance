from django.urls import path

from .views import (
    StudentDetailAPIView,
    StudentListAPIView,
    UpdateStudentAPIView,
    StudentProfileAPIView,
)

urlpatterns = [
    path(
        "student_profile/student_profile/", StudentProfileAPIView.as_view(), name="Student-details"
    ),
    path("all_student/", StudentListAPIView.as_view(), name="all-Student"),
    path(
        "student/<str:username>/", StudentDetailAPIView.as_view(), name="Student-details"
    ),
    path(
        "update_student/<str:username>/", UpdateStudentAPIView.as_view(), name="Student-update"
    ),

]
