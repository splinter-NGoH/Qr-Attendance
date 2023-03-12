from rest_framework.exceptions import APIException


class NotYourDoctor(APIException):
    status_code = 403
    default_detail = "You can't edit a Doctor that doesn't belong to you!"


class CantFollowYourself(APIException):
    status_code = 403
    default_detail = "You can't follow yourself"
