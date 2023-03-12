# from multiprocessing import context
# from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

# from authors_api.settings.production import DEFAULT_FROM_EMAIL

from .exceptions import  NotYourStudent
from .models import Student
from .pagination import StudentPagination
from .renderers import StudentJSONRenderer, StudentsJSONRenderer
from .serializers import  StudentSerializer, UpdateStudentSerializer

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

        data = request.data
        serializer = UpdateStudentSerializer(
            instance=request.user.student, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

