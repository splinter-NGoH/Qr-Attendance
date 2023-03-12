from rest_framework.exceptions import APIException


class UpdateMeal(APIException):
    status_code = 403
    default_detail = "You can't update a meal that does not belong to you'"
class CreateMeal(APIException):
    status_code = 403
    default_detail = "You can't create a meal unless you have chef account'"
class UpdateMealChef(APIException):
    status_code = 403
    default_detail = "You can't update a meal unless you have chef account'"
