from django.urls import path

from .views import (
    StudentDetailAPIView,
    StudentListAPIView,
    UpdateStudentAPIView,
    StudentProfileAPIView,
    CreateStudentAttendance,
    StudentAttendanceReport,
    StudentAttendanceReportByUsername,
    StudentAttendanceReportByUser
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
    path(
        "create_student_attendance/<str:uuid>/", CreateStudentAttendance.as_view(), name="create-student-attendance"
    ),
    path(
        "get_student_attendances/", CreateStudentAttendance.as_view(), name="get-student-attendance"
    ),
    path(
        "attendance_report_by_course/<str:course>/", StudentAttendanceReport.as_view(), name="get-student-report"
    ),
    path(
        "attendance_report_by_username_and_course/<str:course>/<str:username>/", StudentAttendanceReportByUsername.as_view(), name="get-student-report-by-username"
    ),
    path(
        "attendance_report_by_user_and_course/<str:course>/", StudentAttendanceReportByUser.as_view({'get':'list'}), name="get-student-report-by-user"
    ),
]
