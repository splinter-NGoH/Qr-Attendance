from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from qr_code.users.api.views import UserViewSet

from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet,  FCMDeviceViewSet




if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
