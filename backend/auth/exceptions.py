from fastapi import HTTPException, status


class EmailAlreadyRegistered(HTTPException):
    def __init__(self, status_code = status.HTTP_409_CONFLICT, detail = 'Email is already registered', headers = None):
        super().__init__(status_code, detail, headers)


class EmailOrPasswordIncorrect(HTTPException):
    def __init__(self, status_code = status.HTTP_401_UNAUTHORIZED, detail = 'Email or password is incorrect', headers = {"WWW-Authenticate": "Bearer"}):
        super().__init__(status_code, detail, headers)