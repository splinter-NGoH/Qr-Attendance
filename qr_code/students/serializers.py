from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Student


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

