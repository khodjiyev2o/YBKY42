from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidTimeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid time.")
    default_code = "Invalid time."
