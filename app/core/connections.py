from fastapi import WebSocket
from app.annotations import DeviceID
import asyncio


class ConnectionManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.connections: dict[DeviceID, WebSocket] = {}

    async def connect(self, device_id: DeviceID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[device_id] = websocket

    async def disconnect(self, device_id: DeviceID) -> None:
        await self.connections[device_id].close()
        self.connections.pop(device_id)

    async def send_to(self, *device_ids: DeviceID, message: str) -> None:
        await asyncio.gather(
            *(
                self.connections[device_id].send_text(message)
                for device_id in device_ids
            )
        )
