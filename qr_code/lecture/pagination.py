from rest_framework.pagination import PageNumberPagination


class AttendancePagination(PageNumberPagination):
    page_size = 5
