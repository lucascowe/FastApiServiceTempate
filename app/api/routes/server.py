import logging

from fastapi import APIRouter
from app.core.config import settings
from app.core.response_factory import ResponseFactory
from app.models.responses import VersionResponse, StatusResponse

router = APIRouter(prefix="/server")


logger = logging.getLogger(__name__)


@router.get("/version", response_model=VersionResponse)
def get_server_version():
    try:
        version_response = VersionResponse(
            name=settings.server_name,
            version=settings.version
        )
        logger.info(f"VR: {version_response.to_dict()}")
        response = ResponseFactory.json_response(
            version_response
        )
        logger.info(f"Response: {response}")
        return response
    except Exception as e:
        logger.error(f"Exception", exc_info=True)
        raise e

@router.get("/status", response_model=StatusResponse)
def get_server_version():
    logger.info(f"DBS: {settings.databases.keys()}")
    return ResponseFactory.json_response(
        StatusResponse(
            name=settings.server_name,
            version=settings.version,
            services=list(settings.databases.keys())
        ).to_dict()
    )
