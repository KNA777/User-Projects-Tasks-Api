from fastapi import HTTPException


class CustomExceptions(Exception):
    detail = "Error"

    def __init__(self, **kwargs):
        super().__init__(self.detail, **kwargs)


class ObjectNotFoundException(CustomExceptions):
    detail = "Wrong email exception"


class UserPasswordException(ObjectNotFoundException):
    detail = "Wrong password exception"



class ObjectAlreadyExistsException(CustomExceptions):
    detail = "Object exist exception"


class SuperUserPasswordException(CustomExceptions):
    detail = "Wrong superuser password registration exception"


class CustomHTTPExceptions(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class SuperUserPasswordHTTPException(CustomHTTPExceptions):
    status_code = 409
    detail = "Wrong superuser password registration exception"


class UserNotFoundHTTPException(CustomHTTPExceptions):
    status_code = 404
    detail = "User not found exception"


class PasswordHTTPException(CustomHTTPExceptions):
    status_code = 422
    detail = "Wrong password exception"


class MailAlreadyExistHTTPException(CustomHTTPExceptions):
    status_code = 422
    detail = "Mail already exist exception"


class MailHTTPException(CustomHTTPExceptions):
    status_code = 422
    detail = "Wrong mail exception"


class TaskExistsHTTPException(CustomHTTPExceptions):
    status_code = 404
    detail = "Task exist exception"


