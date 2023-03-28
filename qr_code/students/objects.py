from datetime import datetime, timedelta
import pytz


class CreateStudentAttendanceObject (object):
    

    def __init__(self, attendance_request):
        self.attendance_request = attendance_request
        self.cur_time = datetime.now(pytz.timezone("Africa/Cairo") )

        
    def qrcode_not_valid(self):
        cairo = pytz.timezone("Africa/Cairo") 
        max_valid_time = timedelta(minutes=self.attendance_request.period) + self.attendance_request.created_at
        if self.cur_time  > max_valid_time:
            return True