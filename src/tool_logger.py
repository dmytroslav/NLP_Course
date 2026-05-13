import json
import os
from datetime import datetime
import uuid

class ToolLogger:
    def __init__(self, log_file="data/tool_logs_lab12.jsonl"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log_call(self, task_id, tool_name, tool_input, tool_output, success, error=None):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "tool_name": tool_name,
            "input": tool_input,
            "output": tool_output,
            "success": success,
            "error": error
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")