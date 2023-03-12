from django.apps import AppConfig


class LectureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qr_code.lecture'
    verbose_name = "lectures"
    def ready(self):
        try:
            import qr_code.lecture.signals  
        except ImportError:
            pass
