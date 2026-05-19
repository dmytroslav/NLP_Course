from .flow_state import FlowState

class IngestNode:
    def process(self, case_id: str, raw_text: str) -> FlowState:
        # Базова ініціалізація та очищення
        clean_text = raw_text.strip()
        state = FlowState(case_id=case_id, raw_text=raw_text, clean_text=clean_text)
        
        if not clean_text:
            state.errors.append("Input text is empty.")
            
        state.steps_log.append({
            "step": "ingest", 
            "status": "ok", 
            "output_keys": ["case_id", "raw_text", "clean_text"]
        })
        return state