
from django.core.validators import validate_email as validate_email_prebuilt
from django.contrib import messages
from django.core.exceptions import ValidationError


def validate_email(email):
    """
    Validating email provided by the user has correct syntax or not

    @:param email: pass email to validate
    :return: Boolean
    """
    try:
        validate_email_prebuilt(email)
        return True
    except ValidationError:
        raise Exception("Enter a valid Email!")
