from django.urls import path

from .views import (
    DoctorDetailAPIView,
    DoctorListAPIView,
    UpdateDoctorAPIView,
    DoctorProfileAPIView,
    SendNotification,
)

urlpatterns = [
    path(
        "doctor/doctor_profile/", DoctorProfileAPIView.as_view(), name="doctor-details"
    ),
    path("all/", DoctorListAPIView.as_view(), name="all-doctor"),
    path("send_notifications/", SendNotification.as_view(), name="send-doctor"),
    path(
        "user/<str:username>/", DoctorDetailAPIView.as_view(), name="doctor-detail"
    ),
    path(
        "update/<str:username>/", UpdateDoctorAPIView.as_view(), name="doctor-update"
    ),

]
