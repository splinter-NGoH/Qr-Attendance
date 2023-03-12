from rest_framework.pagination import PageNumberPagination


class DoctorPagination(PageNumberPagination):
    page_size = 5
