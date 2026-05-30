from datetime import datetime
from typing import List, Optional

class PipelineTracker:
    def __init__(self):
        self.is_running: bool = False
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None
        self.total_to_process: int = 0
        self.processed_count: int = 0
        self.failed_count: int = 0
        self.currently_processing: Optional[str] = None
        self.errors: List[str] = []

    def start(self, total: int) -> None:
        self.is_running = True
        self.started_at = datetime.utcnow()
        self.finished_at = None
        self.total_to_process = total
        self.processed_count = 0
        self.failed_count = 0
        self.currently_processing = None
        self.errors = []

    def update_progress(self, shortcode: str) -> None:
        self.currently_processing = shortcode

    def complete_post(self, success: bool, error_msg: Optional[str] = None) -> None:
        if success:
            self.processed_count += 1
        else:
            self.failed_count += 1
            if error_msg:
                self.errors.append(error_msg)

    def finish(self) -> None:
        self.is_running = False
        self.finished_at = datetime.utcnow()
        self.currently_processing = None


pipeline_tracker = PipelineTracker()
