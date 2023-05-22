# from multiprocessing import context
# from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from fcm_django.models import FCMDevice

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
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from firebase_admin import messaging
from qr_code.courses.models import Course, StudentCourses

class SendNotification(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = CreateStudentAttendanceSerializer
    # ordering_fields = ["-created_at"]
    def post(self, request, **kwargs):
        data = request.data
        message = messaging.Message(
                        notification=messaging.Notification(
                                title=data["title"],
                                body=data["body"],
                        ),
                        )
        try:
            student_courses = StudentCourses.objects.filter(course__id=data["course_id"])
            for student in student_courses:
                FCMDevice.objects.filter(user=student.user).send_message(
                                message
                                )           
        except Exception as e:
            return Response({"Error": e}, status=status.HTTP_201_CREATED)


        # try:
        #     attendance_request = AttendanceRequest.objects.get(id=uuid)
        # except AttendanceRequest.DoesNotExist:
        #     raise NotFound("AttendanceRequest does not exist")
        # # Add check if student scaned before can't scan more than one time
        # create_student_attendance = CreateStudentAttendanceObject(attendance_request, request=request)
        # if create_student_attendance.qrcode_not_valid():
        #     raise InvalidQrcode
        # if  create_student_attendance.duplicate():
        #     raise DuplicateQrcode
        # data = request.data
        # data["attendance_request"] = attendance_request.pkid
        # data["student"] = Student.objects.get(user=request.user).pkid
        # data["lecture"] = attendance_request.lecture.pkid
        # data["course"] = attendance_request.course.pkid
        # data["status"] = StudentAttendance.Status.ACCEPTED
        # serializer = CreateStudentAttendanceSerializer(data=data, context={"request": request})
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # formatted_response = {
        #     "status_code": status.HTTP_200_OK,
        #     "student_attendance_request": {
        #     "id":serializer.data["id"],
        #     "status":"Added Succeffully"
        #     }
        # }
        return Response({"Success":"Notification Sent Successfully"}, status=status.HTTP_201_CREATED)

