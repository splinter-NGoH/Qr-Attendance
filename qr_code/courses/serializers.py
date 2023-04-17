from rest_framework import serializers

from qr_code.courses.models import Course, StudentCourses
# from sett_elkol.comments.serializers import CommentListSerializer
# from sett_elkol.ratings.serializers import RatingSerializer

# from .custom_tag_field import TagRelatedField


class StudentCoursesSerializer(serializers.ModelSerializer):
    course_info = serializers.SerializerMethodField(read_only=True)
    def get_course_info(self, obj):
        return {
            "title": obj.course.title,
            "slug": obj.course.slug,
            "description": obj.course.description,
            "banner_image": obj.course.banner_image.url,    
            "list_of_doctors": obj.course.list_of_doctors,
        }
    class Meta:
        model = StudentCourses
        exclude = ["updated_at", "pkid"]


class CourseSerializer(serializers.ModelSerializer):
    # courses_to_students = StudentCoursesSerializer(many=True, read_only=True)
    doctors = serializers.SerializerMethodField()
    banner_image = serializers.SerializerMethodField()
    # user = serializers.StringRelatedField(many=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_banner_image(self, obj):
        return obj.banner_image.url

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
    def get_doctors(self, obj):
        return obj.list_of_doctors
    def get_doctor_info(self, obj):
        return {
            "username": obj.user.username,
            # "fullname": obj.user.get_full_name,
            "email": obj.user.email,
            "age": obj.user.doctor.age,
            "chef_photo": obj.user.doctor.doctor_photo.url,    
        }
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            # "price",
            # "tagList",
            "description",
            "banner_image",
            # "doctor_info",
            # "user",
            "created_at",
            "updated_at",
            "doctors",
        ]

