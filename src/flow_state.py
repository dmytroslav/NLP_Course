from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class FlowState:
    case_id: str
    raw_text: str
    clean_text: Optional[str] = None
    route: Optional[str] = None
    routing_reason: Optional[str] = None
    execute_output: Dict[str, Any] = field(default_factory=dict)
    validation_result: Dict[str, Any] = field(default_factory=dict)
    fallback_triggered: bool = False
    export_output: Optional[Dict[str, Any]] = None
    final_status: str = "initialized"
    steps_log: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "raw_text": self.raw_text,
            "clean_text": self.clean_text,
            "route": self.route,
            "routing_reason": self.routing_reason,
            "execute_output": self.execute_output,
            "validation_result": self.validation_result,
            "fallback_triggered": self.fallback_triggered,
            "export_output": self.export_output,
            "final_status": self.final_status,
            "steps_log": self.steps_log,
            "errors": self.errors,
            "warnings": self.warnings
        }