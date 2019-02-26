import re


# GLOBAL REGULAR EXPRESSIONS
EMAIL_VALIDATOR = "^\S+@\S+$"
NAME_VALIDATOR = "^\S+$"
PASSWORD_VALIDATOR = "^\S+$"


def validator(field_type, value):
    switch = {
        "email": True if re.search(EMAIL_VALIDATOR, value) else False,
        "firstname": True if re.search(NAME_VALIDATOR, value) else False,
        "lastname": True if re.search(NAME_VALIDATOR, value) else False,
        "password": True if re.search(PASSWORD_VALIDATOR, value) else False
    }

    return switch[field_type]
