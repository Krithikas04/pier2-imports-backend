from collections.abc import Callable
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.error.exceptions import CustomException, DatabaseError

from src.config import settings


class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Any:
        try:
            return await call_next(request)

        except SQLAlchemyError as exc:
            return self._handle_error(
                request,
                500,
                "Something went wrong",
                f"SQLAlchemyError: {str(getattr(exc, 'orig', exc))}",
            )

        except CustomException as exc:
            status_code = exc.code
            message = exc.message if status_code != 500 else "Something went wrong"
            errors = exc.errors if status_code != 500 else None
            log_message = (
                "Database error"
                if isinstance(exc, DatabaseError) and not settings.DEBUG
                else exc.message
            )

            return self._handle_error(
                request, status_code, message, f"CustomException: {log_message}", errors
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            return self._handle_error(
                request,
                500,
                "Something went wrong",
                f"Unhandled Exception: {repr(exc)}",
            )

    def _get_client_ip(self, request: Request) -> str:
        return request.headers.get(
            "X-Forwarded-For",
            request.client.host if request.client else "unknown",
        )

    def _handle_error(
        self,
        request: Request,
        status_code: int,
        message: str,
        log_message: str,
        errors: Any = None,
    ) -> JSONResponse:
        # logger.error(log_message, client_ip=self._get_client_ip(request))
        print(f"Error: {log_message}, Client IP: {self._get_client_ip(request)}")
        response = JSONResponse(
            status_code=status_code,
            content={
                "message": message or "Something went wrong",
                "errors": errors,
            },
        )
        return response
