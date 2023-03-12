from django.urls import path

from .views import (
    CourseListAPIView,
    StudentCourseListAPIView,
    CourseDetailView,
    get_my_followers,
)

urlpatterns = [
    path("course/", CourseListAPIView.as_view(), name="all"),
    path("student_courses/", StudentCourseListAPIView.as_view(), name="all-trending"),
    path("detail/<slug:slug>/", CourseDetailView.as_view(), name="create"),
    path("current_student_courses/", get_my_followers, name="student-courses"),
]
