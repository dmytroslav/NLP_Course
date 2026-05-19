# Memory & Knowledge Policy (Lab 14)

1. **State Definition**: The `FlowState` object strictly stores case-level data required for the current execution pipeline.
2. **Transient Data**: Raw input and intermediate execution outputs are retained only for the duration of the current run.
3. **Data Isolation**: Intermediate invalid outputs or hallucinated fields are explicitly logged as errors or warnings and are not propagated as verified truth to the export stage.
4. **Knowledge Resources**: Verification schemas, source credibility registries, and routing definitions are treated as read-only knowledge files. The flow cannot mutate these resources during runtime.
5. **Security**: API keys and external credentials are injected via environment variables and are strictly prohibited from being serialized into the flow state or written to `flow_logs_lab14.jsonl`.
6. **State Pollution Prevention**: Each case initializes a fresh `FlowState` instance. Data is passed strictly downstream; previous case states do not influence subsequent runs.