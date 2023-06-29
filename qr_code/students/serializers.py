from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Student, StudentAttendance


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    student_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Student
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "student_photo",
            "phone_number",
            "about_me",
            "gender",
            "country",
            "age",
            "student_id",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_student_photo(self, obj):
        return obj.user.student_photo.url


class UpdateStudentSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Student
        fields = [
            "phone_number",
            "student_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "age",
            "student_id",

        ]


class CreateStudentAttendanceSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = StudentAttendance
        fields = [
            "id",
            "student",
            "lecture",
            "course",
            "attendance_request",
            "status",
            "week_no",
            "created_at",
     
        ]

    def get_created_at(self, obj):
        then = obj.created_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date



class ListStudentAttendanceSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    student_id = serializers.CharField(source="student.id")
    student_name = serializers.CharField(source="student.user.first_name")
    lecture_id = serializers.CharField(source="lecture.id")
    course_id = serializers.CharField(source="course.id")
    attendance_request_id = serializers.CharField(source="attendance_request.id")

    class Meta:
        model = StudentAttendance
        fields = [
            "id",
            "student_id",
            "student_name",
            "lecture_id",
            "course_id",
            "attendance_request_id",
            "status",
            "created_at",
     
        ]

    def get_created_at(self, obj):
        then = obj.created_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

from qr_code.courses.models import Course, StudentCourses


class StudentAtendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="user.username")
    week_1 = serializers.SerializerMethodField()
    week_2 = serializers.SerializerMethodField()
    week_3 = serializers.SerializerMethodField()
    week_4 = serializers.SerializerMethodField()
    week_5 = serializers.SerializerMethodField()
    week_6 = serializers.SerializerMethodField()
    week_7 = serializers.SerializerMethodField()
    week_8 = serializers.SerializerMethodField()
    week_9 = serializers.SerializerMethodField()
    week_10 = serializers.SerializerMethodField()
    week_11 = serializers.SerializerMethodField()
    week_12 = serializers.SerializerMethodField()
    week_13 = serializers.SerializerMethodField()
    week_14 = serializers.SerializerMethodField()
    week_15 = serializers.SerializerMethodField()
    week_16 = serializers.SerializerMethodField()
    week_17 = serializers.SerializerMethodField()
    week_18 = serializers.SerializerMethodField()


    class Meta:
        model = StudentCourses
        fields = [
            "student_name",
            "week_1",
            "week_2",
            "week_3",
            "week_4",
            "week_5",
            "week_6",
            "week_7",
            "week_8",
            "week_9",
            "week_10",
            "week_11",
            "week_12",
            "week_13",
            "week_14",
            "week_15",
            "week_16",
            "week_17",
            "week_18",
     
        ]

    # def get_created_at(self, obj):
    #     then = obj.created_at
    #     formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
    #     return formatted_date
    def get_week_1(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=1).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_2(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=2).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_3(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=3).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_4(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=4).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_5(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=5).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_6(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=6).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_7(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=7).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_8(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=8).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_9(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=9).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_10(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=10).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_11(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=11).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_12(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=12).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_13(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=13).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_14(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=14).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_15(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=15).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_16(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=16).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_17(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=17).exists()
        if students:
            return "Present"
        else:
            return "Absent"
    def get_week_18(self, obj):
        students = StudentAttendance.objects.filter(student=obj.user.student,status="accepted",week_no=18).exists()
        if students:
            return "Present"
        else:
            return "Absent"

