import math
from typing import Any, Callable, Awaitable
from urllib.parse import parse_qs

from lecture_1.hw import utils
from lecture_1.hw.http_response import send_error, ERROR_422, ERROR_400, send_json_response
from lecture_1.hw.utils import receive_body


async def handle_factorial(scope: dict[str, Any], _: Callable[[], Awaitable[dict[str, Any]]],
                           send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    query_string = scope.get("query_string", b"").decode()
    query_params = parse_qs(query_string)

    try:
        n = int(query_params.get("n", [""])[0])
    except ValueError:
        return await send_error(send, ERROR_422)

    if n < 0:
        return await send_error(send, ERROR_400)

    res = math.factorial(n)
    await send_json_response(send, {"result": res})


async def handle_fibonacci(scope: dict[str, Any], _: Callable[[], Awaitable[dict[str, Any]]],
                           send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    path = scope["path"]
    split_path = path.strip("/").split("/")

    try:
        if len(split_path) != 2:
            raise ValueError
        n = int(split_path[1])
    except ValueError:
        return await send_error(send, ERROR_422)

    if n < 0:
        return await send_error(send, ERROR_400)

    res = utils.fibonacci(n)
    await send_json_response(send, {"result": res})


async def handle_mean(_: dict[str, Any], receive: Callable[[], Awaitable[dict[str, Any]]],
                      send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    body = await receive_body(receive)

    if not isinstance(body, list):
        return await send_error(send, ERROR_422)

    if not body:
        return await send_error(send, ERROR_400)

    if not all(isinstance(item, (float, int)) for item in body):
        return await send_error(send, ERROR_422)

    res = sum(body) / len(body)
    await send_json_response(send, {"result": res})
