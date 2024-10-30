import json
from typing import Callable, Awaitable, Tuple

ERROR_400 = (400, "400 Bad Request")
ERROR_404 = (404, "404 Not Found")
ERROR_422 = (422, "422 Unprocessable Entity")

async def send_error(send: Callable[[dict], Awaitable[None]], error: Tuple[int, str]) -> None:
    status, body = error

    await send({
        "type": "http.response.start",
        "status": status,
        "headers": [
            [b"content-type", b"text/plain"]
        ]
    })
    await send({
        "type": "http.response.body",
        "body": body.encode()
    })


async def send_json_response(send, body: any):
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"application/json"),
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps(body).encode()
        }
    )
