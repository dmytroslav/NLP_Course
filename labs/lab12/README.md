# Lab 12: Tool-Grounded Single-Agent

1. **Use case:** Автоматизований Fact-Checker новин.
2. **Agent task:** Класифікація тексту на FAKE/TRUE на основі зовнішніх баз даних.
3. **Tools:** `check_source_credibility`, `get_official_fact`.
4. **Як запускати notebook:** Відкрити `notebooks/lab12_tool_grounded_single_agent.ipynb` у Google Colab, додати GROQ API KEY та запустити "Run All".
5. **Де лежать logs:** `/data/tool_logs_lab12.jsonl`
6. **Test cases:** 10 сценаріїв (включаючи noisy text, missing data, ambiguity, unnecessary calls).
7. **Метрики:** Success Rate: 100%, Avg calls/task: ~1.5. Деталі у `docs/audit_summary_lab12.md`.
8. **Головний висновок:** Надання моделі жорстко зафіксованих інструментів та презумпції фейку дозволяє створити надійну систему класифікації, яка майже повністю позбавлена класичних LLM-галюцинацій.