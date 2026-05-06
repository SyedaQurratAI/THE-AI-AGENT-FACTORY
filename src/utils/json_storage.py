import os
from src.core.config import settings
from src.models.task import ExtractedTask
from src.utils.file_io import save_json, load_json

class TaskStorage:
    def __init__(self):
        self.file_path = os.path.join(settings.DATA_DIR, "tasks.json")

    def save_task(self, task: ExtractedTask):
        tasks = load_json(self.file_path) or []
        tasks.append(task.model_dump(mode="json"))
        save_json(tasks, self.file_path)

task_storage = TaskStorage()
