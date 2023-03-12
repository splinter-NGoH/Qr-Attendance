import logging

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from qr_code.courses.models import Course, StudentCourses

from .exceptions import UpdateMeal, CreateMeal, UpdateMealChef
# from .filters import MealFilter
from .pagination import CoursePagination
from .permissions import IsOwnerOrReadOnly
from .renderers import CourseJSONRenderer, CoursesJSONRenderer
from .serializers import (
    StudentCoursesSerializer,
    CourseSerializer,
)
from qr_code.users.models import User

User = get_user_model()

logger = logging.getLogger(__name__)


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Course.objects.all()
    renderer_classes = (CoursesJSONRenderer,)
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_class = MealFilter
    ordering_fields = ["created_at", "username"]

class StudentCourseListAPIView(generics.ListAPIView):
    serializer_class = StudentCoursesSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StudentCourses.objects.all()
    renderer_classes = (CoursesJSONRenderer,)
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_class = MealFilter
    ordering_fields = ["-created_at"]



class CourseDetailView(APIView):
    renderer_classes = [CourseJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        course = Course.objects.get(slug=slug)
        serializer = CourseSerializer(course, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_my_followers(request):
    try:
        specific_user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        raise NotFound("User does not exist")

    student_courses = StudentCourses.objects.filter(user__pkid=specific_user.pkid)

    serializer = StudentCoursesSerializer(student_courses, many=True)
    formatted_response = {
        "status_code": status.HTTP_200_OK,
        "student_courses": serializer.data,
        "num_of_courses": len(serializer.data),
    }

    return Response(formatted_response, status=status.HTTP_200_OK)

