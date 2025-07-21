import re


PASSWORD_COMPLEXITY_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?_&])[A-Za-z\d@$!%*?_&]{8,}$'


def validator_password_complexity(password: str) -> str | None:
    if not re.fullmatch(PASSWORD_COMPLEXITY_PATTERN, password):
        raise ValueError(
            """Password doesn't meet the requirements. Please use:
            - Minimum 8 characters
            - At least 1 uppercase letter (A-Z)
            - At least 1 lowercase letter (a-z)
            - At least 1 number (0-9)
            - At least 1 special character (@$!%*?_&)"""
        )

    return password