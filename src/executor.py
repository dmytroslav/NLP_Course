import json
from typing import Callable
from .flow_state import FlowState

class ExecutorNode:
    def __init__(self, llm_client: Callable[[str], str]):
        self.llm_client = llm_client

    def process(self, state: FlowState) -> FlowState:
        if state.route != "analyze_news":
            state.steps_log.append({"step": "executor", "status": "skipped"})
            return state

        prompt = f"""
        Act as a professional fact-checker. Extract sources and facts from the text, and classify the news.
        Provide the output EXACTLY matching this JSON schema:
        {{
            "verdict": "True" | "False" | "Fake" | "Unknown",
            "sources": ["source1", ...],
            "facts": ["fact1", ...],
            "confidence": float (0.0 to 1.0)
        }}
        
        Text: "{state.raw_text}"
        """
        
        raw_response = self.llm_client(prompt)
        
        try:
            state.execute_output = json.loads(raw_response)
        except json.JSONDecodeError:
            state.execute_output = raw_response  # Will trigger fallback in Validator
            state.warnings.append("Executor returned unstructured text")

        state.steps_log.append({"step": "executor", "status": "executed"})
        return state