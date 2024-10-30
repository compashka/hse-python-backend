from typing import Any, Awaitable, Callable

from lecture_1.hw.handlers import handle_factorial, handle_fibonacci, handle_mean
from lecture_1.hw.http_response import send_error, ERROR_404


async def app(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    if scope['type'] == 'http' and scope['method'] == 'GET':
        path = scope["path"]
        split_path = path.strip("/").split("/")
        match split_path[0]:
            case 'factorial':
                return await handle_factorial(scope, receive, send)
            case 'fibonacci':
                return await handle_fibonacci(scope, receive, send)
            case 'mean':
                return await handle_mean(scope, receive, send)

    return await send_error(send, ERROR_404)
