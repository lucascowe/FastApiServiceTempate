from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import signal
import sys
import asyncio

from app.core.db import connect_db, close_db
from app.models.responses import StatusResponse
from app.core.config import settings


logger = logging.getLogger(__name__)


main_loop = None


def setup_signal_handlers():
    global main_loop
    main_loop = asyncio.get_event_loop()

    def handle_signal(sig, frame):
        logger.info(f"Received signal {sig}, initiating shutdown...")
        # Schedule the shutdown coroutine on the existing event loop
        if main_loop and main_loop.is_running():
            logger.info(f"Adding shutdown to running loop")
            main_loop.create_task(shutdown_wrapper())
        else:
            # Fallback for when the loop isn't running
            logger.info(f"Starting loop for shutdown")
            temp_loop = asyncio.new_event_loop()
            temp_loop.run_until_complete(shutdown())
            temp_loop.close()
            sys.exit(0)

    async def shutdown_wrapper():
        await shutdown()
        # Stop the event loop after shutdown completes
        main_loop.stop()

    # Register the handlers
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)


async def startup(app: FastAPI):
    # Add startup process here
    await connect_db(app)
    logger.info(f"{settings.server_name} is ready")
    service_info = StatusResponse(
        name=settings.server_name,
        version=settings.api_version,
        services=list(settings.databases.keys()),
        timestamp=None
    )
    logger.info(f"Service info: {service_info.__dict__}")
    print(f"Service info: {service_info.__dict__}")
    setup_signal_handlers()


async def shutdown(app: FastAPI):
    # Add shutdown process here
    await close_db(app)
    pending = asyncio.all_tasks(asyncio.get_event_loop())
    pending.discard(asyncio.current_task())
    await asyncio.gather(*pending, return_exceptions=True)
    logger.info(f"{settings.server_name} is shutdown")


@asynccontextmanager
async def service_lifespan(app: FastAPI):
    await startup(app)
    yield
    await shutdown(app)
