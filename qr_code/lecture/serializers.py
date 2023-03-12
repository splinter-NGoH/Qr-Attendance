from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import QRCode, AttendanceRequest, Lectures

class QrCodesSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    attendance_request = serializers.CharField(source="attendance_request.id")

    class Meta:
        model = QRCode
        fields = ["attendance_request", "qrcode", "updated_at"]

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

class AttendanceRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    email = serializers.EmailField(source="user.email")
    lecture_id = serializers.CharField(source="lecture.id")
    lecture_title = serializers.CharField(source="lecture.title")
    lecture_floor = serializers.CharField(source="lecture.floor")
    lecture_lecture_no = serializers.CharField(source="lecture.lecture_no")
    course_id = serializers.CharField(source="course.id")
    course_title = serializers.CharField(source="course.title")
    course_slug = serializers.CharField(source="course.slug")
    course_banner_image = serializers.CharField(source="course.banner_image.url")
    profile_photo = serializers.SerializerMethodField()
    cur_qrcode = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRequest
        fields = [
            "username",
            "first_name",
            "email",
            "id",
            "profile_photo",
            "lecture_id",
            "lecture_title",
            "lecture_floor",
            "lecture_lecture_no",
            "course_id",
            "course_title",
            "course_slug",
            "course_banner_image",
            "period",
            "cur_qrcode",
            "created_at",
            "updated_at",
        ]


    def get_profile_photo(self, obj):
        return obj.user.doctor.doctor_photo.url

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
    def get_cur_qrcode(self, obj):
        current_qrcodes = obj.qr_codes.all()
        serializer = QrCodesSerializer(current_qrcodes, many=True)
        return serializer.data

class LectureViewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lectures
        exclude = ["updated_at", "pkid"]


class CreateAttendanceRequestSerializer(serializers.ModelSerializer):
    cur_qrcode = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AttendanceRequest
        fields = ["id", "user", "lecture", "course", "period", "cur_qrcode"]

    def get_cur_qrcode(self, obj):
        current_qrcodes = obj.qr_codes.all()
        serializer = QrCodesSerializer(current_qrcodes, many=True)
        return serializer.data
