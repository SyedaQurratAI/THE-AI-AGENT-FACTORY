import asyncio
import signal
from src.gateway.client import OpenClawGatewayClient
from src.core.filter import message_filter
from src.extraction.gemini_client import extraction_client
from src.extraction.prompt_manager import prompt_manager
from src.extraction.normalizer import normalizer
from src.models.task import ExtractedTask
from src.utils.json_storage import task_storage
from src.utils.md_generator import md_generator
from src.utils.logger import logger

async def main():
    client = OpenClawGatewayClient()

    async def handle_message(message_data):
        if message_filter.should_process(message_data):
            text = message_filter.get_message_text(message_data)
            if not text:
                return

            logger.info(f"Extracting task from: {text}")
            
            # 1. Extract using Gemini
            prompt = prompt_manager.get_task_extraction_prompt()
            raw_result = await extraction_client.extract_task(text, prompt)
            
            if not raw_result or not raw_result.get("is_task"):
                logger.debug("No task detected in message.")
                return

            # 2. Normalize and Validate
            try:
                task = ExtractedTask(
                    source_jid=message_data["params"].get("jid") or message_data["params"]["message"].get("from"),
                    original_text=text,
                    task_description=raw_result["task_description"],
                    assignee=raw_result.get("assignee", "unknown"),
                    deadline=normalizer.normalize_deadline(raw_result.get("deadline")),
                    confidence_score=raw_result.get("confidence_score", 0.0),
                    status="processed"
                )
                logger.info(f"Successfully extracted task: {task.task_description}")
                
                # 3. Store results
                task_storage.save_task(task)
                md_generator.add_task(task)
                logger.info(f"Task persisted to JSON and Markdown.")

            except Exception as e:
                logger.error(f"Failed to process and store task: {e}")

    # Set the handler (note: changed to async handler)
    client.on_message_received = lambda msg: asyncio.create_task(handle_message(msg))

    # Handle shutdown signals
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(client.disconnect()))
        except NotImplementedError:
            # signal handlers are not implemented on Windows with some loops
            pass

    try:
        await client.connect()
    except asyncio.CancelledError:
        logger.info("Main loop cancelled.")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
