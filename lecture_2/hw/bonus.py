from dataclasses import field, dataclass
from uuid import uuid4, UUID

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Bonus Websocket")

@dataclass(slots=True)
class Chat:
    subscribers: list[WebSocket] = field(init=False, default_factory=list)

    async def subscribe(self, ws: WebSocket) -> None:
        await ws.accept()
        self.subscribers.append(ws)

    async def unsubscribe(self, ws: WebSocket) -> None:
        self.subscribers.remove(ws)

    async def publish(self, client_id: UUID, message: str, publisher: WebSocket = None) -> None:
        text = f"{client_id} :: {message}"
        for ws in self.subscribers:
            if ws != publisher:
                await ws.send_text(text)


chats: dict[str, Chat] = {}

@app.websocket("/chat/{chat_name}")
async def ws_chat(ws: WebSocket, chat_name: str):
    client_id = uuid4()
    if chat_name not in chats:
        chats[chat_name] = Chat()

    chat_room = chats[chat_name]
    await chat_room.subscribe(ws)
    await chat_room.publish(client_id, "subscribed")
    try:
        while True:
            text = await ws.receive_text()
            await chat_room.publish(client_id, text, ws)
    except WebSocketDisconnect:
        await chat_room.unsubscribe(ws)
        await chat_room.publish(client_id, "unsubscribed")
