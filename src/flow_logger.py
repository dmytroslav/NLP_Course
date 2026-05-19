import json
import os
from typing import Dict, Any

class FlowLogger:
    def __init__(self, log_path: str = "docs/flow_logs_lab14.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_case(self, state_dict: Dict[str, Any]) -> None:
        log_entry = {
            "case_id": state_dict.get("case_id"),
            "input": state_dict.get("raw_text"),
            "steps": state_dict.get("steps_log"),
            "route": state_dict.get("route"),
            "validation_result": state_dict.get("validation_result"),
            "fallback_triggered": state_dict.get("fallback_triggered"),
            "export_output": state_dict.get("export_output"),
            "final_status": state_dict.get("final_status"),
            "errors": state_dict.get("errors"),
            "warnings": state_dict.get("warnings")
        }
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")