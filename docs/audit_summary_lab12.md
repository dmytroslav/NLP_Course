# Audit Summary (Lab 12: Tool-grounded single-agent)

## 1. Архітектура
- **Use case:** Fact-Checking Agent для аналізу новин.
- **Tools:** `check_source_credibility`, `get_official_fact`.
- **Test cases:** 10

## 2. Метрики
- Tool call success rate: 100.0%
- Average tool calls per task: 0.8
- Tasks with useful tool use: 8
- Unnecessary tool calls: 1

## 3. Найкращі / Проблемні приклади
- **Найкращі:** Кейс 3 (Noisy text) та Кейс 7 (подвійний виклик). Агент успішно проігнорував капс і правильно визначив пропаганду.
- **Проблемні:** Кейс 5 (Агент перевіряв загальновідомий факт про столицю) та Кейс 10 (Конфлікт джерел "Офіційно від Трухи").

## 4. Висновки та покращення
Tools критично знизили галюцинації. Для покращення потрібно додати логіку ранжування джерел (щоб вирішувати конфлікти в тексті) та заборонити виклик інструментів для географічних/загальновідомих фактів.

## Error Analysis (10 cases)

1. **Case 01 (Simple)**: Expected TRUE. Actual: TRUE. Error: None. Fix: N/A.
2. **Case 02 (Missing data)**: Expected TRUE (через слово "Офіційно"). Actual: FAKE. Category: `tool output ignored`. Агент не повірив офіційному джерелу через відсутність факту в базі. Fix: Жорсткіше прописати пріоритет офіційних джерел.
3. **Case 03 (Noisy)**: Expected FAKE. Actual: FAKE. Error: None.
4. **Case 04 (Empty Return)**: Expected FAKE. Actual: FAKE. Error: None.
5. **Case 05 (Unnecessary call)**: Agent checked "Київ столиця". Category: `unnecessary tool call`. Fix: Add prompt rule to skip tools for common knowledge.
6. **Case 06 (Ambiguity)**: Expected TRUE ("Міністерство оборони"). Actual: FAKE. Category: `tool output ignored`. Модель заплуталась через складну конструкцію речення. Fix: Навчити модель краще аналізувати складнопідрядні речення.
7. **Case 07 (Two tools)**: Expected FAKE. Actual: FAKE. Error: None.
8. **Case 08 (Validator)**: Expected FAKE. Actual: FAKE. Error: None.
9. **Case 09 (Ref tool)**: Expected TRUE. Actual: TRUE. Error: None.
10. **Case 10 (Agent mistake)**: Input had conflicting sources ("Офіційно" and "Труха"). Category: `agent hallucinates / over-trusts tool`. Fix: Add conflict resolution logic to prompt.

