import logging
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("auth_api")


async def unhandled_exception_handler(request: Request, exc: Exception):
    error_id = str(uuid.uuid4())
    logger.exception(
        "Unhandled error error_id=%s method=%s path=%s",
        error_id,
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_id": error_id,
        },
    )
