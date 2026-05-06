import asyncio
import json
import pytest
import websockets
from src.gateway.client import OpenClawGatewayClient
from src.core.config import settings

@pytest.mark.asyncio
async def test_gateway_connection_and_handshake():
    # Mock WebSocket server
    async def mock_server(websocket):
        # Receive handshake
        message = await websocket.recv()
        data = json.loads(message)
        assert data["method"] == "connect"
        
        # Send a mock message event
        await websocket.send(json.dumps({
            "event": "message.received",
            "params": {
                "message": {
                    "from": "12345@g.us",
                    "text": "Hello Aina!"
                }
            }
        }))

    # Start mock server
    server = await websockets.serve(mock_server, "localhost", 18790)
    
    # Update settings for test
    settings.GATEWAY_URL = "ws://localhost:18790"
    client = OpenClawGatewayClient()
    received_messages = []

    def handle_message(msg):
        received_messages.append(msg)

    client.on_message_received = handle_message
    
    # Run client connect in a task so we can cancel it
    connect_task = asyncio.create_task(client.connect())
    
    # Wait for message to be processed
    for _ in range(10):
        if received_messages:
            break
        await asyncio.sleep(0.1)

    assert len(received_messages) == 1
    assert received_messages[0]["params"]["message"]["text"] == "Hello Aina!"
    
    # Cleanup
    connect_task.cancel()
    server.close()
    await server.wait_closed()
