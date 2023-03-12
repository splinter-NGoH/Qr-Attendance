from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    doctor_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Doctor
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "doctor_photo",
            "phone_number",
            "about_me",
            "gender",
            "country",
            "city",
            "age",

        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = ""
        if obj.user.last_name:
            last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_doctor_photo(self, obj):
        return obj.doctor_photo.url


class UpdateDoctorSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Doctor
        fields = [
            "phone_number",
            "doctor_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "age",

        ]

