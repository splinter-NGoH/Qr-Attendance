from django.contrib import admin

from . import models


class LecturesAdmin(admin.ModelAdmin):
    list_display = ["pkid", "title", "slug", "floor", "lecture_no"]
    list_display_links = ["pkid", "slug"]


admin.site.register(models.Lectures, LecturesAdmin)

class AttendanceRequestAdmin(admin.ModelAdmin):
    list_display = ["pkid", "lecture", "course", "period"]
    list_display_links = ["pkid", "lecture"]


admin.site.register(models.AttendanceRequest, AttendanceRequestAdmin)
class QRCodeRequestAdmin(admin.ModelAdmin):
    list_display = ["pkid", "attendance_request", "qrcode"]
    list_display_links = ["pkid", "attendance_request"]


admin.site.register(models.QRCode, QRCodeRequestAdmin)
