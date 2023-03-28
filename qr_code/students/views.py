# from multiprocessing import context
# from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

# from authors_api.settings.production import DEFAULT_FROM_EMAIL

from .exceptions import  NotYourStudent, IsStudentOrReadOnly, InvalidQrcode
from .models import Student, StudentAttendance
from .pagination import StudentPagination
from .renderers import StudentJSONRenderer, StudentsJSONRenderer
from .serializers import  StudentSerializer, UpdateStudentSerializer, CreateStudentAttendanceSerializer
from .objects import CreateStudentAttendanceObject
from qr_code.lecture.models import AttendanceRequest
User = get_user_model()


class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Student.objects.all()
    renderer_classes = (StudentsJSONRenderer,)
    pagination_class = StudentPagination


class StudentDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.select_related("user")
    serializer_class = StudentSerializer
    renderer_classes = (StudentJSONRenderer,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            student = self.queryset.get(user__username=username)
        except Student.DoesNotExist:
            raise NotFound("A Student with this username does not exist")

        serializer = self.serializer_class(student, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.select_related("user")
    serializer_class = StudentSerializer
    renderer_classes = (StudentJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        try:
            student = self.queryset.get(user=request.user)
        except Student.DoesNotExist:
            raise NotFound("A Student with this username does not exist")

        serializer = self.serializer_class(student, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateStudentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.select_related("user")
    renderer_classes = [StudentJSONRenderer]
    serializer_class = UpdateStudentSerializer

    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Student.DoesNotExist:
            raise NotFound("A Student with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourStudent
    #ee
        data = request.data
        serializer = UpdateStudentSerializer(
            instance=request.user.student, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateStudentAttendance(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = CreateStudentAttendanceSerializer
    ordering_fields = ["-created_at"]

    def get(self, request):
        try:
            specific_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        student_attendance_request = StudentAttendance.objects.filter(student__user__pkid=specific_user.pkid).order_by("-created_at")
        serializer = CreateStudentAttendanceSerializer(student_attendance_request, many=True)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "student_attendance_request": serializer.data,
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

    def post(self, request,uuid, **kwargs):
        try:
            attendance_request = AttendanceRequest.objects.get(id=uuid)
        except AttendanceRequest.DoesNotExist:
            raise NotFound("AttendanceRequest does not exist")
        # Add check if student scaned before can't scan more than one time
        create_student_attendance = CreateStudentAttendanceObject(attendance_request)
        if create_student_attendance.qrcode_not_valid():
            raise InvalidQrcode
        data = request.data
        data["attendance_request"] = attendance_request.pkid
        data["student"] = Student.objects.get(user=request.user).pkid
        data["lecture"] = attendance_request.lecture.pkid
        data["course"] = attendance_request.course.pkid
        data["status"] = StudentAttendance.Status.ACCEPTED
        serializer = CreateStudentAttendanceSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
