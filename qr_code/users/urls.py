from django.urls import path

from qr_code.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    ActivateAccount,
    LogoutView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:uid>/<str:token>/", view=ActivateAccount.as_view(), name="activate"),

]
