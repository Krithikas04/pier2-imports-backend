from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from src.core.helpers.constants import ALLOWED_ORIGIN
from src.config import settings
from src.core.di import Container
from src.core.middleware import (
    CustomErrorMiddleware,
    validation_exception_handler,
)
from src.routers import api_router


class FastAPIApp:
    def __init__(self) -> None:
        self.app = FastAPI(
            title="Pier 2 Imports API",
            description="Backend system for Pier 2 Imports order management",
            version=settings.APP_VERSION,
            debug=settings.DEBUG,
            docs_url=None if settings.APP_ENV == "prod" else "/docs",
            redoc_url=None if settings.APP_ENV == "prod" else "/redoc",
        )

        self._init_middlewares()
        self.container = self._init_dependency_container()
        self.app.container = self.container  # type: ignore

    # -------------------------
    # Middleware Setup
    # -------------------------
    def _init_middlewares(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=ALLOWED_ORIGIN if settings.APP_ENV == "prod" else ["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"],
        )

        self.app.add_middleware(CustomErrorMiddleware)
        # self.app.add_middleware(ResponseMiddleware)

    # -------------------------
    # Dependency Injection
    # -------------------------
    def _init_dependency_container(self) -> Container:
        return Container()

    # -------------------------
    # Router Initialization
    # -------------------------
    def _init_routers(self) -> None:
        self.app.include_router(
            api_router,
            prefix=f"/api/{settings.APP_VERSION}",
        )
    # -------------------------
    # App Factory
    # -------------------------
    def create_app(self) -> FastAPI:
        self._init_routers()

        self.app.add_exception_handler(
            RequestValidationError,
            validation_exception_handler,
        )

        return self.app


# Application instance
fastapi_app = FastAPIApp()
app = fastapi_app.create_app()
