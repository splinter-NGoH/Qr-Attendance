from django.urls import path
from .views import CustomRegistrationView
from qr_code.users.views import (
    LogoutView,
)

urlpatterns = [
    path("register/", CustomRegistrationView.as_view({'post': 'create'})),
    path('logout/', LogoutView.as_view(), name='auth_logout'),

]
