import json
import os
from typing import List, Any
from src.utils.logger import logger

def save_json(data: Any, file_path: str):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.debug(f"Successfully saved JSON to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")

def load_json(file_path: str) -> Any:
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {file_path}: {e}")
        return None

def append_to_markdown(text: str, file_path: str):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception as e:
        logger.error(f"Failed to append to Markdown at {file_path}: {e}")
