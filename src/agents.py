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
    def __init__(self, client, model="llama3-8b-8192"):
        self.client = client
        self.model = model
        self.system_prompt = """Ти - Reviewer. Перевір JSON, згенерований Extractor.
        Шукай галюцинації (вигадані джерела) або пропущені маркери. 
        Якщо є проблеми, verdict має бути 'repair_needed'. Якщо все ідеально - 'accept'.
        ОБОВ'ЯЗКОВО ПОВЕРНИ ВІДПОВІДЬ У ФОРМАТІ JSON:
        {
            "verdict": "accept|repair_needed|manual_review",
            "valid_json": true,
            "consistency_ok": boolean,
            "issues": [{"field": "назва поля", "problem": "опис"}],
            "recommended_action": "string"
        }"""

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