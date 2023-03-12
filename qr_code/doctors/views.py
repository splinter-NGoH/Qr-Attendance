# from multiprocessing import context
# from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

# from authors_api.settings.production import DEFAULT_FROM_EMAIL

from .exceptions import  NotYourDoctor
from .models import Doctor
from .pagination import DoctorPagination
from .renderers import DoctorJSONRenderer, DoctorsJSONRenderer
from .serializers import DoctorSerializer, UpdateDoctorSerializer

User = get_user_model()


class DoctorListAPIView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Doctor.objects.all()
    renderer_classes = (DoctorsJSONRenderer,)
    pagination_class = DoctorPagination


class DoctorDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doctor.objects.select_related("user")
    serializer_class = DoctorSerializer
    renderer_classes = (DoctorJSONRenderer,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            doctor = self.queryset.get(user__username=username)
        except Doctor.DoesNotExist:
            raise NotFound("A Doctor with this username does not exist")

        serializer = self.serializer_class(doctor, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doctor.objects.select_related("user")
    serializer_class = DoctorSerializer
    renderer_classes = (DoctorJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        try:
            doctor = self.queryset.get(user=request.user)
        except Doctor.DoesNotExist:
            raise NotFound("A Doctor with this profile does not exist")

        serializer = self.serializer_class(doctor, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateDoctorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doctor.objects.select_related("user")
    renderer_classes = [DoctorJSONRenderer]
    serializer_class = UpdateDoctorSerializer

    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Doctor.DoesNotExist:
            raise NotFound("A Doctor with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourDoctor

        data = request.data
        serializer = UpdateDoctorSerializer(
            instance=request.user.doctor, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

