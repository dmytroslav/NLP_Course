import json
from typing import Callable, Any
from .flow_state import FlowState

class RouterNode:
    def __init__(self, llm_client: Callable[[str], str]):
        self.llm_client = llm_client

    def process(self, state: FlowState) -> FlowState:
        prompt = f"""
        Analyze the following text. Determine if it is a news claim that requires fact-checking.
        Respond ONLY with a valid JSON format.
        Schema: {{"route": "analyze_news" | "skip", "reason": "string"}}
        
        Text to analyze: "{state.raw_text}"
        """
        
        raw_response = self.llm_client(prompt)
        
        try:
            response_data = json.loads(raw_response)
            state.route = response_data.get("route", "skip")
            state.routing_reason = response_data.get("reason", "No reason provided")
        except json.JSONDecodeError:
            state.route = "analyze_news" 
            state.routing_reason = "Failed to parse routing response, defaulting to analysis"
            state.warnings.append("Router JSON parse error")

        state.steps_log.append({"step": "router", "route": state.route})
        return state