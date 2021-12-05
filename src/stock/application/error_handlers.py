import datetime
from typing import Any, Callable, Coroutine

from fastapi import Request
from fastapi.responses import JSONResponse


async def _internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": str(datetime.datetime.now()),
            "reason": "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.",
            "path": request.url.path,
        },
    )


def get_error_handlers() -> list[Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]]:
    return [_internal_server_error_handler]
