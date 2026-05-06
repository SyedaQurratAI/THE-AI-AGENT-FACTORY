import os
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    OPENCLAW_API_KEY: str
    GEMINI_API_KEY: str
    GATEWAY_URL: str = "ws://localhost:18789"
    MONITORED_JIDS_STR: str = ""
    DATA_DIR: str = "data"
    LOG_LEVEL: str = "INFO"

    @property
    def MONITORED_JIDS(self) -> List[str]:
        if not self.MONITORED_JIDS_STR:
            return []
        return [jid.strip() for jid in self.MONITORED_JIDS_STR.split(",") if jid.strip()]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
