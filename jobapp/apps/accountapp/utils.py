import re


def check_identifier(identifier):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.match(email_pattern, identifier):
        return "email"
    else:
        return "username"


def is_valid_email(email):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    return bool(re.match(email_pattern, email))


def is_valid_password(password):
    password_pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>_-])[A-Za-z0-9!@#$%^&*(),.?":{}|<>_-]{8,20}$'
    return bool(re.match(password_pattern, password))
