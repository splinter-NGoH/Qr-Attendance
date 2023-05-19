from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # Activate Account
    path("activate/", include("qr_code.users.urls", namespace="activation")),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("qr_code.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet,  FCMDeviceViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)
router.register('devices_v2',  FCMDeviceViewSet)

# API URLS
urlpatterns += [
    # API base url
    path('fcm_django/', include(router.urls)),

    path("api/", include("config.api_router")),

    # DRF auth token
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # apps urls
    # path("api/v1/doctors/", include("qr_code.doctors.urls")),
    path("api/v1/", include("users.api.urls")),
    path("api/v1/students-profiles/", include("qr_code.students.urls")),
    path("api/v1/doctors-profiles/", include("qr_code.doctors.urls")),
    path("api/v1/courses/", include("qr_code.courses.urls")),
    path("api/v1/lectures/", include("qr_code.lecture.urls")),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # path("api/v1/meals/", include("sett_elkol.meal.urls")),

]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    # if "debug_toolbar" in settings.INSTALLED_APPS:
    #     import debug_toolbar

    #     urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
admin.site.site_header = "Qr Attendance"
admin.site.site_title = "Qr Attendance Admin Portal"
admin.site.index_title = "Welcome to the Qr Attendance Portal"
