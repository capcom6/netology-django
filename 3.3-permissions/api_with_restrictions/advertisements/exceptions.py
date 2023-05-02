from rest_framework import exceptions, status


class OpenAdvertisementsLimitException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You have reached the maximum number of open advertisements."


class SelfFavoriteException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You can not add your own advertisement to favorites."
