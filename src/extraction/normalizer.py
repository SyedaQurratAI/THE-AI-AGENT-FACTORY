from datetime import datetime
from typing import Optional
from src.utils.logger import logger

class TaskNormalizer:
    @staticmethod
    def normalize_deadline(deadline_str: Optional[str]) -> Optional[datetime]:
        if not deadline_str:
            return None
        try:
            # Gemini should return ISO 8601, but we validate and parse it
            return datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
        except Exception as e:
            logger.warning(f"Failed to normalize deadline '{deadline_str}': {e}")
            return None

normalizer = TaskNormalizer()
