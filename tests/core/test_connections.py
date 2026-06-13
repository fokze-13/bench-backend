import pytest
from app.core.connections import ConnectionManager
from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from unittest.mock import AsyncMock, PropertyMock
from uuid import uuid4

@pytest.mark.anyio
async def test_connection_manager_connect():
    manager = ConnectionManager()
    manager.connections.clear()
    
    device_id = str(uuid4())
    websocket = AsyncMock(spec=WebSocket)
    
    await manager.connect(device_id, websocket)
    
    websocket.accept.assert_called_once()
    assert manager.connections[device_id] == websocket

@pytest.mark.anyio
async def test_connection_manager_disconnect():
    manager = ConnectionManager()
    manager.connections.clear()
    
    device_id = str(uuid4())
    websocket = AsyncMock(spec=WebSocket)
    type(websocket).client_state = PropertyMock(return_value=WebSocketState.CONNECTED)
    
    await manager.connect(device_id, websocket)
    await manager.disconnect(device_id)
    
    websocket.close.assert_called_once()
    assert device_id not in manager.connections

@pytest.mark.anyio
async def test_connection_manager_send_to():
    manager = ConnectionManager()
    manager.connections.clear()
    
    device_id1 = str(uuid4())
    websocket1 = AsyncMock(spec=WebSocket)
    
    device_id2 = str(uuid4())
    websocket2 = AsyncMock(spec=WebSocket)
    
    await manager.connect(device_id1, websocket1)
    await manager.connect(device_id2, websocket2)
    
    message = {"type": "test", "payload": {}}
    await manager.send_to(device_id1, device_id2, python_obj_message=message)
    
    websocket1.send_json.assert_called_once_with(message)
    websocket2.send_json.assert_called_once_with(message)
