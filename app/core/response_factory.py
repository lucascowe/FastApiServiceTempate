import logging
from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException, status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    FileResponse,
    StreamingResponse,
    RedirectResponse,
    PlainTextResponse
)
from fastapi.encoders import jsonable_encoder
import os


logger = logging.getLogger(__name__)


class ResponseFactory:
    """
    A factory class to create different types of FastAPI responses.py.
    Centralizes response handling and formatting for consistency across API endpoints.
    """

    @staticmethod
    def json_response(
            content: Any,
            status_code: int = status.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None
    ) -> JSONResponse:
        """
        Create a JSON response with the given content, status code, and headers.

        Args:
            content: The content to be returned (will be converted to JSON)
            status_code: HTTP status code (default: 200 OK)
            headers: Optional dictionary of headers

        Returns:
            JSONResponse: A FastAPI JSONResponse object
        """
        # Convert content to a JSON-compatible format
        logger.info(f"Converting {content}")
        json_content = jsonable_encoder(content)
        logger.info(f"Converted {content}")

        return JSONResponse(
            content=json_content,
            status_code=status_code,
            headers=headers
        )

    @staticmethod
    def html_response(
            content: str,
            status_code: int = status.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None
    ) -> HTMLResponse:
        """
        Create an HTML response with the given content, status code, and headers.

        Args:
            content: HTML content string
            status_code: HTTP status code (default: 200 OK)
            headers: Optional dictionary of headers

        Returns:
            HTMLResponse: A FastAPI HTMLResponse object
        """
        return HTMLResponse(
            content=content,
            status_code=status_code,
            headers=headers
        )

    @staticmethod
    def file_response(
            path: str,
            filename: Optional[str] = None,
            media_type: Optional[str] = None,
            status_code: int = status.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None
    ) -> FileResponse:
        """
        Create a file download response.

        Args:
            path: Path to the file to be served
            filename: Optional filename to use in the Content-Disposition header
            media_type: Optional media type (if not provided, it will be guessed)
            status_code: HTTP status code (default: 200 OK)
            headers: Optional dictionary of headers

        Returns:
            FileResponse: A FastAPI FileResponse object

        Raises:
            HTTPException: If the file does not exist
        """
        if not os.path.isfile(path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {filename or path}"
            )

        return FileResponse(
            path=path,
            filename=filename,
            media_type=media_type,
            status_code=status_code,
            headers=headers
        )

    @staticmethod
    def streaming_response(
            content: Any,
            media_type: str,
            status_code: int = status.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None
    ) -> StreamingResponse:
        """
        Create a streaming response (useful for large files or real-time data).

        Args:
            content: A generator or any iterable
            media_type: Media type of the content
            status_code: HTTP status code (default: 200 OK)
            headers: Optional dictionary of headers

        Returns:
            StreamingResponse: A FastAPI StreamingResponse object
        """
        return StreamingResponse(
            content=content,
            media_type=media_type,
            status_code=status_code,
            headers=headers
        )

    @staticmethod
    def text_response(
            content: str,
            status_code: int = status.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None
    ) -> PlainTextResponse:
        """
        Create a plain text response.

        Args:
            content: Text content
            status_code: HTTP status code (default: 200 OK)
            headers: Optional dictionary of headers

        Returns:
            PlainTextResponse: A FastAPI PlainTextResponse object
        """
        return PlainTextResponse(
            content=content,
            status_code=status_code,
            headers=headers
        )

    @staticmethod
    def redirect_response(
            url: str,
            status_code: int = status.HTTP_307_TEMPORARY_REDIRECT,
            headers: Optional[Dict[str, str]] = None
    ) -> RedirectResponse:
        """
        Create a redirect response.

        Args:
            url: URL to redirect to
            status_code: HTTP status code (default: 307 Temporary Redirect)
            headers: Optional dictionary of headers

        Returns:
            RedirectResponse: A FastAPI RedirectResponse object
        """
        return RedirectResponse(
            url=url,
            status_code=status_code,
            headers=headers
        )

    @staticmethod
    def error_response(
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail: str = "Internal Server Error",
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Raise an HTTPException with the given status code, detail, and headers.
        This is used for error responses.py and will be caught by FastAPI's exception handlers.

        Args:
            status_code: HTTP status code (default: 500 Internal Server Error)
            detail: Detail message for the error
            headers: Optional dictionary of headers

        Raises:
            HTTPException: Always raises an HTTPException
        """
        raise HTTPException(
            status_code=status_code,
            detail=detail,
            headers=headers
        )

    @classmethod
    def success_response(
            cls,
            data: Any = None,
            message: str = "Success",
            status_code: int = status.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None
    ) -> JSONResponse:
        """
        Create a standardized success JSON response.

        Args:
            data: Optional data to include in the response
            message: Success message (default: "Success")
            status_code: HTTP status code (default: 200 OK)
            headers: Optional dictionary of headers

        Returns:
            JSONResponse: A standardized success response
        """
        content = {
            "status": "success",
            "message": message,
        }

        if data is not None:
            content["data"] = data

        return cls.json_response(
            content=content,
            status_code=status_code,
            headers=headers
        )

    @classmethod
    def error_json_response(
            cls,
            message: str = "An error occurred",
            status_code: int = status.HTTP_400_BAD_REQUEST,
            error_code: Optional[str] = None,
            errors: Optional[List[Dict[str, Any]]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> JSONResponse:
        """
        Create a standardized error JSON response without raising an exception.

        Args:
            message: Error message
            status_code: HTTP status code (default: 400 Bad Request)
            error_code: Optional application-specific error code
            errors: Optional list of detailed errors
            headers: Optional dictionary of headers

        Returns:
            JSONResponse: A standardized error response
        """
        content = {
            "status": "error",
            "message": message,
        }

        if error_code:
            content["error_code"] = error_code

        if errors:
            content["errors"] = errors

        return cls.json_response(
            content=content,
            status_code=status_code,
            headers=headers
        )