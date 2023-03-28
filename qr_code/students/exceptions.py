from rest_framework.exceptions import APIException


class NotYourStudent(APIException):
    status_code = 403
    default_detail = "You can't edit a Student that doesn't belong to you!"


class IsStudentOrReadOnly(APIException):
    status_code = 403
    default_detail = "You Must Be Student To Scan QRCode"

class InvalidQrcode(APIException):
    status_code = 403
    default_detail = "QrCode Expired"
