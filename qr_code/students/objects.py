from datetime import datetime, timedelta
import pytz

from .models import Student, StudentAttendance

class CreateStudentAttendanceObject (object):
    

    def __init__(self, attendance_request, request):
        self.attendance_request = attendance_request
        self.cur_time = datetime.now(pytz.timezone("Africa/Cairo") )
        self.request = request

        
    def qrcode_not_valid(self):
        max_valid_time = timedelta(minutes=self.attendance_request.period) + self.attendance_request.created_at
        if self.cur_time  > max_valid_time:
            return True
        
    def duplicate(self):

        student_attendance = StudentAttendance.objects.filter(attendance_request=self.attendance_request, student=self.request.user.student)
        return student_attendance