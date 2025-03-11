from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import traceback
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base application exception class"""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def add_exception_handlers(app: FastAPI):
    """Add all exception handlers to the FastAPI app"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Handle custom application exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle FastAPI request validation errors"""
        errors = []
        for error in exc.errors():
            error_msg = {
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", "")
            }
            errors.append(error_msg)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Validation error",
                "errors": errors
            }
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors"""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Data validation error",
                "errors": exc.errors()
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions"""
        # Log the full traceback for debugging
        error_message = f"Unhandled exception: {str(exc)}"
        logger.error(error_message)
        logger.error(traceback.format_exc())

        # In production, return a generic error message
        # In development, you might want to return more details
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"}
        )
