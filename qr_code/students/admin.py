from django.contrib import admin

from .models import Student, StudentAttendance


class StudentAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "gender", "phone_number", "student_id"]
    list_filter = ["gender", "country", "city"]
    list_display_links = ["id", "pkid"]


admin.site.register(Student, StudentAdmin)

class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "student", "lecture", "course", "status"]
    list_filter = ["status"]
    list_display_links = ["id", "pkid"]


admin.site.register(StudentAttendance, StudentAttendanceAdmin)
