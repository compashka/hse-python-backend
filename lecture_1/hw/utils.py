import json
from typing import Callable, Awaitable, Any

async def receive_body(receive: Callable[[], Awaitable[dict[str, Any]]]) -> Any:
    body = b""
    while True:
        message = await receive()
        body += message["body"]
        if not message.get("more_body"):
            break
    try:
        return json.loads(body.decode())
    except json.JSONDecodeError:
        return None

def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
