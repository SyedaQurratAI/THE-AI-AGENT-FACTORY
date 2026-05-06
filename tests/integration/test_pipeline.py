import asyncio
import json
import os
import pytest
import websockets
from unittest.mock import MagicMock, patch
from src.main import main
from src.core.config import settings
from src.extraction.gemini_client import extraction_client

@pytest.mark.asyncio
async def test_full_pipeline_gateway_to_storage():
    # 1. Setup paths and mock server
    test_json = os.path.join(settings.DATA_DIR, "tasks.json")
    test_md = os.path.join(settings.DATA_DIR, "summary.md")
    
    if os.path.exists(test_json): os.remove(test_json)
    if os.path.exists(test_md): os.remove(test_md)

    async def mock_server(websocket):
        await websocket.recv() # connect
        # Send message from monitored JID
        await websocket.send(json.dumps({
            "event": "message.received",
            "params": {
                "jid": "12345@g.us",
                "message": {
                    "text": "Nafees, fix the login bug by tomorrow"
                }
            }
        }))
        await asyncio.sleep(1.0) # Allow processing time

    server = await websockets.serve(mock_server, "localhost", 18790)
    settings.GATEWAY_URL = "ws://localhost:18790"
    settings.MONITORED_JIDS_STR = "12345@g.us"

    # 2. Mock Gemini on the existing singleton instance
    mock_response = MagicMock()
    mock_gemini_resp = {
        "task_description": "fix the login bug",
        "assignee": "Nafees",
        "deadline": "2026-05-06T12:00:00Z",
        "confidence_score": 0.98,
        "is_task": True
    }
    mock_response.text = json.dumps(mock_gemini_resp)

    # Patch the models.generate_content method of the singleton's client
    with patch.object(extraction_client.client.models, 'generate_content', return_value=mock_response) as mock_gen:
        # Run main loop briefly
        main_task = asyncio.create_task(main())
        await asyncio.sleep(2.5) # Increased wait for async tasks
        main_task.cancel()

    # 3. Verify storage
    assert os.path.exists(test_json), "tasks.json should exist"
    assert os.path.exists(test_md), "summary.md should exist"
    
    with open(test_json, "r") as f:
        tasks = json.load(f)
        assert len(tasks) == 1
        assert tasks[0]["task_description"] == "fix the login bug"

    with open(test_md, "r") as f:
        content = f.read()
        assert "fix the login bug" in content

    # Cleanup
    server.close()
    await server.wait_closed()
