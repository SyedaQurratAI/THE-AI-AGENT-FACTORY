import json
from google import genai
from typing import Optional
from pydantic import BaseModel, Field
from src.core.config import settings
from src.utils.logger import logger

class TaskExtractionOutput(BaseModel):
    """Schema for Gemini task extraction output."""
    task_description: str = Field(description="Clear, concise description of the action to be taken")
    assignee: str = Field(description="Name of the person assigned or 'unknown'")
    deadline: Optional[str] = Field(description="ISO 8601 timestamp of the deadline or null")
    confidence_score: float = Field(description="Score between 0.0 and 1.0")
    is_task: bool = Field(description="True if an actionable task was found")

class GeminiExtractionClient:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = 'gemini-1.5-flash'

    async def extract_task(self, text: str, system_prompt: str) -> Optional[dict]:
        try:
            # The new SDK supports response_schema for native structured output
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{system_prompt}\n\nUser Message: \"{text}\"",
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': TaskExtractionOutput,
                }
            )
            
            if response.text:
                return json.loads(response.text)
            return None
        except Exception as e:
            logger.error(f"Gemini extraction failed: {e}")
            return None

extraction_client = GeminiExtractionClient()
