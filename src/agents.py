import json

class TriagerAgent:
    def __init__(self, client, model="llama3-8b-8192"):
        self.client = client
        self.model = model
        self.system_prompt = """Ти - Triager. Твоє завдання: прочитати текст новини, 
        визначити її тематику, рівень складності (low, medium, high) 
        та маршрут ('standard_news' або 'manipulative_text').
        ОБОВ'ЯЗКОВО ПОВЕРНИ ВІДПОВІДЬ У ФОРМАТІ СУВОРОГО JSON:
        {
            "topic": "string",
            "complexity": "low|medium|high",
            "route": "standard_news|manipulative_text",
            "notes": "string"
        }"""

    def run(self, text: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Текст новини:\n{text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)

class ExtractorAgent:
    def __init__(self, client, model="llama3-8b-8192"):
        self.client = client
        self.model = model
        self.system_prompt = """Ти - Extractor. Твоє завдання: витягти структуровані дані з новини.
        СТРОГЕ ПРАВИЛО: Не вигадуй джерела чи твердження. Якщо джерела немає, масив sources_mentioned має бути порожнім.
        ОБОВ'ЯЗКОВО ПОВЕРНИ ВІДПОВІДЬ У ФОРМАТІ СУВОРОГО JSON:
        {
            "main_claim": "string",
            "sources_mentioned": ["string"],
            "emotional_tone": "neutral|emotional|aggressive|panic",
            "manipulation_markers": ["string"],
            "confidence_note": "string"
        }"""

    def run(self, text: str, route: str, notes: str) -> dict:
        prompt = f"Маршрут: {route}\nНотатки Triager: {notes}\n\nТекст новини:\n{text}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)

class ReviewerAgent:
    def __init__(self, client, model="llama-3.1-8b-instant"):
        self.client = client
        self.model = model
        self.system_prompt = """Ти - неупереджений Редактор-Аудитор. Твоє завдання: порівняти оригінальний текст та JSON від Extractor.
        ПРАВИЛА:
        1. НЕ ВИГАДУЙ ПОМИЛОК. Якщо Extractor чесно витягнув те, що є в тексті - це 'accept'.
        2. Якщо в тексті немає джерел, і Extractor залишив масив порожнім [] - це ПРАВИЛЬНО ('accept').
        3. 'repair_needed' став ТІЛЬКИ тоді, коли Extractor додав слово/джерело, якого ФІЗИЧНО немає в оригінальному тексті.
        4. Ти не оцінюєш правдивість самої новини, ти оцінюєш лише якість екстракції.
        
        ОБОВ'ЯЗКОВО ПОВЕРНИ ВІДПОВІДЬ У ФОРМАТІ JSON:
        {
            "verdict": "accept|repair_needed|manual_review",
            "valid_json": true,
            "consistency_ok": boolean,
            "issues": [{"field": "назва поля", "problem": "опис реальної помилки"}],
            "recommended_action": "string"
        }"""

    # ... метод run залишається без змін

    def run(self, text: str, extracted_data: dict) -> dict:
        prompt = f"Оригінальний текст:\n{text}\n\nЗгенерований JSON:\n{json.dumps(extracted_data, ensure_ascii=False)}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)

class FallbackAgent:
    def __init__(self, client, model="llama3-8b-8192"):
        self.client = client
        self.model = model
        self.system_prompt = """Ти - Repair Agent. Отримай сирий текст, попередній JSON та зауваження від Reviewer. 
        Виправ помилки в JSON. Не змінюй правильні поля.
        ПОВЕРНИ ВИПРАВЛЕНИЙ РЕЗУЛЬТАТ У ФОРМАТІ JSON:
        {
            "main_claim": "string",
            "sources_mentioned": ["string"],
            "emotional_tone": "neutral|emotional|aggressive|panic",
            "manipulation_markers": ["string"],
            "confidence_note": "string"
        }"""

    def run(self, text: str, extracted_data: dict, issues: list) -> dict:
        prompt = f"Текст:\n{text}\n\nПопередній JSON:\n{json.dumps(extracted_data, ensure_ascii=False)}\n\nЗауваження Reviewer:\n{json.dumps(issues, ensure_ascii=False)}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)