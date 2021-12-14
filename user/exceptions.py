from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

msg = 'Does Not Exist.'
_status_code = status.HTTP_404_NOT_FOUND

# User
class UserDoesNotExistException(APIException):
    status_code = _status_code
    default_detail = _('User {}'.format(msg))
