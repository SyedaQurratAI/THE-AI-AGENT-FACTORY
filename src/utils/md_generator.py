import os
from src.core.config import settings
from src.models.task import ExtractedTask
from src.utils.file_io import append_to_markdown

class MarkdownGenerator:
    def __init__(self):
        self.file_path = os.path.join(settings.DATA_DIR, "summary.md")
        self._ensure_header()

    def _ensure_header(self):
        if not os.path.exists(self.file_path):
            header = "# Aina Task Summary\n\n| Date | Task | Assignee | Deadline | Source |\n|------|------|----------|----------|--------|\n"
            append_to_markdown(header.strip(), self.file_path)

    def add_task(self, task: ExtractedTask):
        date_str = task.created_at.strftime("%Y-%m-%d %H:%M")
        deadline_str = task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "N/A"
        row = f"| {date_str} | {task.task_description} | {task.assignee} | {deadline_str} | {task.source_jid} |"
        append_to_markdown(row, self.file_path)

md_generator = MarkdownGenerator()
