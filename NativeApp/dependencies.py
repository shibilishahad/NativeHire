import re


def is_valid_password(password):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}"
        return bool(re.match(password_pattern, password))

def phone_no_is_valid(phone_no):
    return phone_no.isdigit() and len(phone_no) == 10