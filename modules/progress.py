import sys
import time
import shutil
from datetime import datetime


class ProgressTracker:
    def __init__(self):
        self.start_time = time.time()
        self.terminal_width = shutil.get_terminal_size().columns
        self.last_update = 0

    def _get_formatted_line(self, text):
        # Ensure line fits terminal width and is properly padded
        return f"\r{text:<{self.terminal_width}}"

    def update_word_progress(self, current_word, current_index, total_words):
        current_time = time.time()
        # Limit updates to max 10 per second to prevent flickering
        if current_time - self.last_update < 0.1:
            return

        self.last_update = current_time
        percentage = (current_index / total_words) * 100

        progress_text = (
            f"Testing: {current_word:<30} "
            f"[{self._progress_bar(percentage)}] "
            f"{percentage:0.1f}% "
            f"({current_index}/{total_words})"
        )

        sys.stdout.write(self._get_formatted_line(progress_text))
        sys.stdout.flush()

    def update_crawl_progress(self, visited_count, queue_size, found_count):
        current_time = time.time()
        if current_time - self.last_update < 0.1:
            return

        self.last_update = current_time

        status_text = (
            f"Processed: {visited_count} pages | "
            f"Queue: {queue_size} pages | "
            f"Found: {found_count} URLs"
        )

        sys.stdout.write(self._get_formatted_line(status_text))
        sys.stdout.flush()

    def _progress_bar(self, percentage, width=20):
        filled = int(width * percentage // 100)
        bar = "█" * filled + "░" * (width - filled)
        return bar

    def clear_line(self):
        sys.stdout.write(self._get_formatted_line(""))
        sys.stdout.flush()
