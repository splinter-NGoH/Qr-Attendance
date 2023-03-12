from multiprocessing import context
from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsDoctorOrReadOnly

# from qr_code.settings.production import DEFAULT_FROM_EMAIL

from .exceptions import MustBeDoctor
from .models import QRCode, Lectures, AttendanceRequest
from qr_code.courses.models import Course

from .pagination import AttendancePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import AttendanceRequestSerializer, LectureViewsSerializer,CreateAttendanceRequestSerializer
User = get_user_model()

class LectureListAPIView(generics.ListAPIView):
    serializer_class = LectureViewsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Lectures.objects.all()
    pagination_class = AttendancePagination
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_class = ArticleFilter
    ordering_fields = ["-created_at"]

class CreateAttendanceRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrReadOnly]
    serializer_class = AttendanceRequestSerializer
    ordering_fields = ["-created_at"]

    def get(self, request):
        try:
            specific_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        attendance_request_instance = AttendanceRequest.objects.filter(user__pkid=specific_user.pkid)
        serializer = AttendanceRequestSerializer(attendance_request_instance, many=True)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "attendance_request_instance": serializer.data,
            "num_attendance_request_instance": len(serializer.data),
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        try:
            specific_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")
        user = request.user
        data = request.data
        data["user"] = user.pkid
        data["lecture"] = Lectures.objects.get(id=data["lecture"]).pkid
        data["course"] = Course.objects.get(id=data["course"]).pkid
        serializer = CreateAttendanceRequestSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
