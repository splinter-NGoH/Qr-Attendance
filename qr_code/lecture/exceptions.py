from rest_framework.exceptions import APIException


class MustBeDoctor(APIException):
    status_code = 403
    default_detail = "You can't you can't add atendance request unless you are a doctor!"


class CantFollowYourself(APIException):
    status_code = 403
    default_detail = "You can't follow yourself"
