# Flow Notes (Lab 14)

1. **Який use case обрано:** Classification & Extraction для новин (True/False/Fake) із витягуванням джерел та фактів.
2. **Які етапи flow:** Ingest → Route → Execute → Validate → Fallback (optional) → Export.
3. **Яка структура state:** Об'єкт `FlowState` (case_id, raw_text, route, validation_result, execute_output, export_output, errors, warnings, steps_log).
4. **Які routes можливі:** `analyze_news` (для перевірки фактів) та `skip` (для побутового спаму).
5. **Що робить execute:** LLM-екстракція джерел та фактів зі строгою типізацією у JSON.
6. **Що перевіряє validate:** Відповідність `jsonschema` (наявність required полів, типи даних).
7. **Коли спрацьовує fallback:** Якщо `execute` повернув невалідний JSON (JSONDecodeError або ValidationError).
8. **Який export format:** Структурований словник `{"status": "...", "data": {...}}`.
9. **Що flow покращив порівняно з ad-hoc pipeline:** Гарантує стабільний JSON на виході (навіть при помилці моделі), відсіює спам на ранньому етапі (маршрутизація), логує кожен крок для дебагу.
10. **Де flow був надлишковим:** Для очевидних загальновідомих фактів (наприклад, Київ — столиця), де можна було б обійтися одним prompt-ом.
11. **Що б ви фіксили далі:** Додав би семантичний кеш (vector store) на етапі Ingest, щоб не викликати LLM для новин, які вже були перевірені раніше.