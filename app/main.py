import json
import logging.config
from fastapi import FastAPI

from app.core.config import settings
from app.api import routes
from app.core.events import service_lifespan

from app.core.exception_handlers import add_exception_handlers
from app.core.middleware import add_middleware


with open('app/core/logging_config.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)



logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.server_name,
    description="FastAPI service template",
    version=settings.version,
    lifespan=service_lifespan
)
app.include_router(router=routes.server_router)
add_middleware(app)
add_exception_handlers(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
