from django.urls import path

from .views import (
    DoctorDetailAPIView,
    DoctorListAPIView,
    UpdateDoctorAPIView,
    DoctorProfileAPIView,
)

urlpatterns = [
    path(
        "doctor/doctor_profile/", DoctorProfileAPIView.as_view(), name="doctor-details"
    ),
    path("all/", DoctorListAPIView.as_view(), name="all-doctor"),
    path(
        "user/<str:username>/", DoctorDetailAPIView.as_view(), name="doctor-detail"
    ),
    path(
        "update/<str:username>/", UpdateDoctorAPIView.as_view(), name="doctor-update"
    ),

]
