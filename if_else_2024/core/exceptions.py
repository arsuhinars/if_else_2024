from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(
        self,
        details: str | None = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.__details = "Unknown error" if details is None else details
        self.__status_code = status_code

    @property
    def details(self):
        return self.__details

    @property
    def status_code(self):
        return self.__status_code

    def __str__(self) -> str:
        return self.__details


class EntityNotFoundException(AppException):
    def __init__(self, entity_class: type | None = None):
        super().__init__(
            (
                "Required entity was not found"
                if entity_class is None
                else f"Required entity '{entity_class.__name__}' was not found"
            ),
            status.HTTP_404_NOT_FOUND,
        )


class EntityAlreadyExistsException(AppException):
    def __init__(self, entity_class: type | None = None):
        super().__init__(
            (
                "Given entity already exists"
                if entity_class is None
                else f"Given entity '{entity_class.__name__}' already exists"
            ),
            status.HTTP_409_CONFLICT,
        )


class UnauthorizedException(AppException):
    def __init__(self, details: str | None = None):
        super().__init__(
            "Unauthorized" if details is None else details,
            status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenException(AppException):
    def __init__(self, details: str | None = None):
        super().__init__(
            "Forbidden" if details is None else details,
            status.HTTP_403_FORBIDDEN,
        )


def handle_app_exception(request: Request, exception: AppException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"details": exception.details},
    )
