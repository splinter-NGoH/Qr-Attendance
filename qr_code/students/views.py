# from multiprocessing import context
# from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count

# from authors_api.settings.production import DEFAULT_FROM_EMAIL

from .exceptions import  NotYourStudent, IsStudentOrReadOnly, InvalidQrcode, DuplicateQrcode
from .models import Student, StudentAttendance
from .pagination import StudentPagination
from .renderers import StudentJSONRenderer, StudentsJSONRenderer
from .serializers import  StudentSerializer, UpdateStudentSerializer, CreateStudentAttendanceSerializer,ListStudentAttendanceSerializer
from .objects import CreateStudentAttendanceObject
from qr_code.lecture.models import AttendanceRequest
from qr_code.courses.models import StudentCourses, Course

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
        serializer = ListStudentAttendanceSerializer(student_attendance_request, many=True)
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
        create_student_attendance = CreateStudentAttendanceObject(attendance_request, request=request)
        if create_student_attendance.qrcode_not_valid():
            raise InvalidQrcode
        if  create_student_attendance.duplicate():
            raise DuplicateQrcode
        data = request.data
        data["attendance_request"] = attendance_request.pkid
        data["student"] = Student.objects.get(user=request.user).pkid
        data["lecture"] = attendance_request.lecture.pkid
        data["course"] = attendance_request.course.pkid
        data["week_no"] = attendance_request.week_no
        data["status"] = StudentAttendance.Status.ACCEPTED
        serializer = CreateStudentAttendanceSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "student_attendance_request": {
            "id":serializer.data["id"],
            "status":"Added Succeffully"
            }
        }
        return Response(formatted_response, status=status.HTTP_201_CREATED)


class StudentAttendanceReport(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    ordering_fields = ["-created_at"]
    def student_attendance(self, request, course, course_type):
        return StudentAttendance.objects.filter(lecture__type=course_type, student__user__pkid=request, course=course).count()
    def get(self, request, course):
        try:
            course_obj = Course.objects.get(id=course)
        except Course.DoesNotExist:
            raise NotFound("Course does not exist")
        try:
            student_course = StudentCourses.objects.filter(user=request.user, course=course_obj.pkid)
        except StudentCourses.DoesNotExist:
            raise NotFound("Student doesn't assigned to this course")
        lectures_count= self.student_attendance(request.user.pkid, course_obj.pkid, course_type="lecture")
        sections_count= self.student_attendance(request.user.pkid, course_obj.pkid, course_type="section")
        formatted_response = {
            
            "status_code": status.HTTP_200_OK,
            "lectures_count": lectures_count,
            "sections_count": sections_count,
            "lectures_percent": (lectures_count / course_obj.session_counts) *100,
            "sections_percent":  (sections_count / course_obj.session_counts) *100,
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

class StudentAttendanceReportByUsername(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    ordering_fields = ["-created_at"]
    def student_attendance(self, request, course, course_type):
        return StudentAttendance.objects.filter(lecture__type=course_type, student__user__username=request, course=course).count()
    def get(self, request, course, username):
        try:
            print(course)
            course_obj = Course.objects.get(id=course)
            
        except Course.DoesNotExist:
            raise NotFound("Course does not exist")
        try:
            student_course = StudentCourses.objects.filter(user__username=username, course=course_obj.pkid)
        except StudentCourses.DoesNotExist:
            raise NotFound("Student doesn't assigned to this course")
        lectures_count= self.student_attendance(username, course_obj.pkid, course_type="lecture")
        sections_count= self.student_attendance(username, course_obj.pkid, course_type="section")
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "lectures_count": lectures_count,
            "sections_count": sections_count,
            "lectures_percent": (lectures_count / course_obj.session_counts) *100,
            "sections_percent":  (sections_count / course_obj.session_counts) *100,
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from .models import StudentAttendance
from .serializers import StudentAtendanceSerializer

class StudentAttendanceReportByUser(XLSXFileMixin, ReadOnlyModelViewSet):
    serializer_class = StudentAtendanceSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'my_export.xlsx'
    def get_queryset(self):
        course = self.kwargs['course']
        cur_course = Course.objects.get(id=course)
        return StudentCourses.objects.filter(course=cur_course.pkid)
    # def get_header(self):
    #     return {
    #     'titles': [
    #         "student_name",
    #         "Column_2_name",
    #         "Column_3_name",
    #     ],
    #     'column_width': [17, 30, 17],
    #     'height': 25,
    #     'style': {
    #         'fill': {
    #             'fill_type': 'solid',
    #             'start_color': 'FFCCFFCC',
    #         },
    #         'alignment': {
    #             'horizontal': 'center',
    #             'vertical': 'center',
    #             'wrapText': True,
    #             'shrink_to_fit': True,
    #         },
    #         'border_side': {
    #             'border_style': 'thin',
    #             'color': 'FF000000',
    #         },
    #         'font': {
    #             'name': 'Arial',
    #             'size': 14,
    #             'bold': True,
    #             'color': 'FF000000',
    #         },
    #     },
    # }