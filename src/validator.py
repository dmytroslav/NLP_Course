import json
from jsonschema import validate, ValidationError
from typing import Dict, Any
from .flow_state import FlowState

NEWS_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["True", "False", "Fake", "Unknown"]},
        "sources": {"type": "array", "items": {"type": "string"}},
        "facts": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["verdict", "sources", "facts", "confidence"]
}

class ValidatorNode:
    def __init__(self, schema: Dict[str, Any] = NEWS_SCHEMA):
        self.schema = schema

    def process(self, state: FlowState) -> FlowState:
        if state.route != "analyze_news":
            return state

        execute_data = state.execute_output
        
        if isinstance(execute_data, str):
            try:
                execute_data = json.loads(execute_data)
            except json.JSONDecodeError as e:
                state.validation_result = {"is_valid": False, "reason": f"JSON Parse Error: {str(e)}"}
                state.fallback_triggered = True
                state.errors.append("Executor returned invalid JSON string.")
                return state

        try:
            validate(instance=execute_data, schema=self.schema)
            state.validation_result = {"is_valid": True, "reason": "Schema validation passed."}
            state.fallback_triggered = False
        except ValidationError as e:
            state.validation_result = {"is_valid": False, "reason": f"Schema Error: {e.message}"}
            state.fallback_triggered = True
            state.errors.append(f"Validation failed on field '{e.json_path}': {e.message}")

        state.steps_log.append({"step": "validator", "is_valid": state.validation_result.get("is_valid")})
        return state