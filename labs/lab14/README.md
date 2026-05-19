# Lab 14: Stateful Flow Orchestration

1. **Use Case:** Stateful-пайплайн для класифікації новин та фактчекінгу.
2. **Етапи flow:** Ingest → Route → Execute → Validate → Export.
3. **State:** Датаклас `FlowState`, який зберігає контекст поточного кейсу та ізолює дані від інших запусків.
4. **Routes:** `analyze_news` (перевірка фактів) та `skip` (побутовий спам).
5. **Validation:** Жорстка перевірка через `jsonschema` (поля `verdict`, `sources`, `facts`, `confidence`).
6. **Fallback:** Запит до LLM на виправлення JSON, якщо валідація не пройдена.
7. **Export format:** Уніфікований Python dict / JSON API response.
8. **Як запускати notebook:** Відкрити `lab14_flow_orchestration_crewai_flows.ipynb` в Google Colab та натиснути "Run All".
9. **Logs:** Файл `docs/flow_logs_lab14.jsonl`.
10. **Metrics:** Flow Completion: 100%, Validation Pass: 100%, Export Valid: 100%.
11. **Головний висновок:** Orchestration pattern (Flow) перетворює нестабільну генеративну модель на надійний інженерний компонент із гарантованим контрактом даних.