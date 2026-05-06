from typing import Optional, Set
from src.core.config import settings
from src.utils.logger import logger

class MessageFilter:
    def __init__(self):
        logger.info("Initialized MessageFilter.")

    @property
    def monitored_jids(self) -> Set[str]:
        return set(settings.MONITORED_JIDS)

    def should_process(self, message_data: dict) -> bool:
        # Extract JID from OpenClaw message payload
        params = message_data.get("params", {})
        message = params.get("message", {})
        
        source_jid = message.get("from") or params.get("jid")
        
        if not source_jid:
            logger.debug("Received message without JID, skipping.")
            return False

        is_monitored = source_jid in self.monitored_jids
        
        if is_monitored:
            logger.info(f"Message from monitored JID {source_jid} accepted.")
        else:
            logger.debug(f"Message from unmonitored JID {source_jid} ignored.")
            
        return is_monitored

    def get_message_text(self, message_data: dict) -> Optional[str]:
        params = message_data.get("params", {})
        message = params.get("message", {})
        return message.get("text") or message.get("body")

message_filter = MessageFilter()
