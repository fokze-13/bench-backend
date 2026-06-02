from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from app.annotations import DeviceID
import asyncio
from typing import Any
import logging
from app.logger import setup_logger

logger = setup_logger(__name__, logging.INFO)


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
        logger.info(f"Device {device_id} connected via websocket")

    async def disconnect(self, device_id: DeviceID) -> None:
        if self.connections[device_id].client_state == WebSocketState.CONNECTED:
            await self.connections[device_id].close()

        self.connections.pop(device_id)
        logger.info(f"Device {device_id} disconnected from websocket")

    async def send_to(self, *device_ids: DeviceID, json_message: Any) -> None:
        await asyncio.gather(
            *(
                self.connections[device_id].send_json(json_message)
                for device_id in device_ids
            )
        )
