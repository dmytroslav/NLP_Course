from typing import Callable, Any, Dict
from .ingest import IngestNode
from .router import RouterNode
from .executor import ExecutorNode
from .validator import ValidatorNode
from .fallback import FallbackNode
from .exporter import ExporterNode

class NewsAnalysisFlow:
    def __init__(self, llm_client: Callable[[str], str]):
        self.ingest = IngestNode()
        self.router = RouterNode(llm_client)
        self.executor = ExecutorNode(llm_client)
        self.validator = ValidatorNode()
        self.fallback = FallbackNode(llm_client)
        self.exporter = ExporterNode()

    def run(self, case_id: str, raw_text: str) -> Dict[str, Any]:
        state = self.ingest.process(case_id, raw_text)
        
        if not state.errors:
            state = self.router.process(state)
            state = self.executor.process(state)
            state = self.validator.process(state)
            
            if state.fallback_triggered:
                state = self.fallback.process(state)
                state = self.validator.process(state) 
                
        state = self.exporter.process(state)
        
        return state.to_dict()