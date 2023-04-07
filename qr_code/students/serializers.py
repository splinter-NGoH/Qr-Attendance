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
        return obj.student_photo.url


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


