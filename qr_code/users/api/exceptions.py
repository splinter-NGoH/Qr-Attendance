from rest_framework.exceptions import APIException


class IfStudentStudentIdReq(APIException):
    status_code = 403
    default_detail = "You Must provide your student id!"


class CantFollowYourself(APIException):
    status_code = 403
    default_detail = "You can't follow yourself"
