import asyncio
import json
import websockets
from typing import Callable, Optional
from src.core.config import settings
from src.utils.logger import logger

class OpenClawGatewayClient:
    def __init__(self):
        self.uri = f"{settings.GATEWAY_URL}?token={settings.OPENCLAW_API_KEY}"
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.on_message_received: Optional[Callable[[dict], None]] = None

    async def connect(self):
        try:
            logger.info(f"Connecting to OpenClaw Gateway at {settings.GATEWAY_URL}...")
            self.websocket = await websockets.connect(self.uri)
            
            # Handshake
            await self.websocket.send(json.dumps({
                "type": "req",
                "id": "1",
                "method": "connect",
                "params": {"role": "operator"}
            }))
            
            logger.info("Connected and authenticated with OpenClaw Gateway.")
            await self.listen()
        except Exception as e:
            logger.error(f"Failed to connect to Gateway: {e}")
            await asyncio.sleep(5)
            await self.connect()

    async def listen(self):
        if not self.websocket:
            return

        async for message in self.websocket:
            try:
                data = json.loads(message)
                # Filter for message events (adjust based on actual OpenClaw event schema)
                if data.get("event") == "message.received" or data.get("method") == "onMessage":
                    if self.on_message_received:
                        self.on_message_received(data)
            except Exception as e:
                logger.error(f"Error processing message from Gateway: {e}")

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected from OpenClaw Gateway.")
