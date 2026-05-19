from .flow_state import FlowState

class ExporterNode:
    def process(self, state: FlowState) -> FlowState:
        if state.route == "skip":
            state.export_output = {
                "status": "skipped",
                "reason": state.routing_reason,
                "data": None
            }
            state.final_status = "completed_skipped"
            state.steps_log.append({"step": "exporter", "status": "skipped"})
            return state

        is_valid = state.validation_result.get("is_valid", False)

        if is_valid:
            state.export_output = {
                "status": "success",
                "data": state.execute_output
            }
            state.final_status = "completed_success"
        else:
            state.export_output = {
                "status": "failed",
                "reason": state.validation_result.get("reason", "Validation failed"),
                "data": {
                    "verdict": "Unknown",
                    "sources": [],
                    "facts": [],
                    "confidence": 0.0
                }
            }
            state.final_status = "completed_with_errors"

        state.steps_log.append({"step": "exporter", "status": "exported"})
        return state