import pytest
from unittest.mock import MagicMock, patch
from src.extraction.gemini_client import GeminiExtractionClient
from src.extraction.prompt_manager import prompt_manager
from src.extraction.normalizer import normalizer

@pytest.mark.asyncio
async def test_extraction_logic():
    # Mock the response object from google-genai
    mock_response = MagicMock()
    mock_response.text = '{"task_description": "finish the report", "assignee": "Nafees", "deadline": "2026-05-08T17:00:00", "confidence_score": 0.95, "is_task": true}'
    
    # Patch the Client class
    with patch("google.genai.Client") as mock_client_class:
        # Configure the mock client instance
        mock_client_instance = mock_client_class.return_value
        mock_client_instance.models.generate_content.return_value = mock_response
        
        client = GeminiExtractionClient()
        result = await client.extract_task("Nafees, please finish the report by Friday 5 PM", "system prompt")
        
        assert result["task_description"] == "finish the report"
        assert result["assignee"] == "Nafees"
        assert result["is_task"] is True
        
        # Verify the call was made correctly
        mock_client_instance.models.generate_content.assert_called_once()

def test_normalization():
    deadline_str = "2026-05-08T17:00:00Z"
    normalized = normalizer.normalize_deadline(deadline_str)
    assert normalized.year == 2026
    assert normalized.month == 5
    assert normalized.day == 8
    assert normalized.hour == 17
