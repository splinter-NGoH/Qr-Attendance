from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from djoser.views import UserViewSet
from .serializers import CreateUserSerializer
from djoser import signals, utils
from djoser.conf import settings
from djoser.compat import get_user_email
from .exceptions import IfStudentStudentIdReq
User = get_user_model()


# class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = "username"

#     def get_queryset(self, *args, **kwargs):
#         assert isinstance(self.request.user.id, int)
#         return self.queryset.filter(id=self.request.user.id)

#     @action(detail=False)
#     def me(self, request):
#         serializer = UserSerializer(request.user, context={"request": request})
#         return Response(status=status.HTTP_200_OK, data=serializer.data)


class CustomRegistrationView(UserViewSet):
    def perform_create(self, serializer, **kwargs):

        super(CustomRegistrationView,self).perform_create(serializer)
    
    def get_serializer_class(self):

        return CreateUserSerializer