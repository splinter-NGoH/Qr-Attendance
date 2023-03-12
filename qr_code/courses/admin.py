from django.contrib import admin

from .models import StudentCourses, Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "title", "slug"]
    list_filter = ["user"]
    list_display_links = ["id", "pkid"]


admin.site.register(Course, CourseAdmin)
class StudentCoursesAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "course"]
    list_filter = ["user"]
    list_display_links = ["id", "pkid"]


admin.site.register(StudentCourses, StudentCoursesAdmin)
