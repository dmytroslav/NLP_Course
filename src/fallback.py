import json
from typing import Callable
from .flow_state import FlowState

class FallbackNode:
    def __init__(self, llm_client: Callable[[str], str]):
        self.llm_client = llm_client

    def process(self, state: FlowState) -> FlowState:
        if not state.fallback_triggered or state.route != "analyze_news":
            return state

        error_reason = state.validation_result.get("reason", "Unknown validation error")
        invalid_data = state.execute_output

        prompt = f"""
        You are a JSON repair assistant. The previous extraction failed validation.
        Error: {error_reason}
        Invalid Data: {invalid_data}
        Original Text: "{state.raw_text}"
        
        Fix the JSON to strictly match this schema:
        {{
            "verdict": "True" | "False" | "Fake" | "Unknown",
            "sources": ["source1", ...],
            "facts": ["fact1", ...],
            "confidence": float (0.0 to 1.0)
        }}
        Output ONLY valid JSON.
        """
        
        raw_response = self.llm_client(prompt)
        
        try:
            state.execute_output = json.loads(raw_response)
            state.warnings.append("Fallback applied successfully to parse JSON.")
        except json.JSONDecodeError:
            state.execute_output = raw_response
            state.errors.append("Fallback failed to produce valid JSON.")

        state.steps_log.append({"step": "fallback", "status": "executed"})
        return state