import json
from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# 1. СХЕМИ ДАНИХ (Pydantic Models)
# ==========================================

class TriagerOutput(BaseModel):
    topic: str = Field(description="Тематика новини (наприклад: війна, політика, економіка, суспільство)")
    complexity: str = Field(description="Складність для аналізу: low, medium, high")
    route: str = Field(description="Маршрут: 'standard_news' або 'manipulative_text'")
    notes: Optional[str] = Field(description="Нотатки для Extractor (на що звернути увагу)")

class ExtractorOutput(BaseModel):
    main_claim: Optional[str] = Field(description="Головне твердження або меседж новини")
    sources_mentioned: List[str] = Field(default_factory=list, description="Список джерел, згаданих у тексті")
    emotional_tone: str = Field(description="Тон тексту: neutral, emotional, aggressive, panic")
    manipulation_markers: List[str] = Field(default_factory=list, description="Знайдені маркери (наприклад: клікбейт, узагальнення, апеляція до емоцій)")
    confidence_note: str = Field(description="Коментар щодо впевненості екстракції")

class ReviewIssue(BaseModel):
    field: str = Field(description="Назва проблемного поля (наприклад, 'sources_mentioned')")
    problem: str = Field(description="Опис проблеми (наприклад, 'Джерело вигадане, в тексті його немає')")

class ReviewerOutput(BaseModel):
    verdict: str = Field(description="Одне зі значень: 'accept', 'repair_needed', 'manual_review'")
    valid_json: bool = Field(description="Чи пройшов JSON базову валідацію")
    consistency_ok: bool = Field(description="Чи не суперечать витягнуті дані оригінальному тексту")
    issues: List[ReviewIssue] = Field(default_factory=list, description="Список знайдених логічних або структурних помилок")
    recommended_action: Optional[str] = Field(description="Що має зробити Fallback агент")

# ==========================================
# 2. КЛАСИ АГЕНТІВ (Agent Definitions)
# ==========================================

class TriagerAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.system_prompt = """Ти - Triager. Твоє завдання: прочитати текст новини, 
        визначити її тематику, рівень складності (чи є прихований підтекст) 
        та маршрут ('standard_news' або 'manipulative_text'). Не роби екстракцію сам."""

    def run(self, text: str) -> dict:
        prompt = f"{self.system_prompt}\n\nТекст новини:\n{text}"
        # Тут ми викликаємо LLM з structured output (TriagerOutput)
        response = self.llm.with_structured_output(TriagerOutput).invoke(prompt)
        return response.dict()

class ExtractorAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.system_prompt = """Ти - Extractor. Твоє завдання: витягти структуровані дані з тексту новини.
        СТРОГЕ ПРАВИЛО: Не вигадуй джерела чи твердження. Якщо джерела немає, залишай масив порожнім."""

    def run(self, text: str, route: str, notes: str) -> dict:
        prompt = f"{self.system_prompt}\n\nМаршрут: {route}\nНотатки Triager: {notes}\n\nТекст новини:\n{text}"
        response = self.llm.with_structured_output(ExtractorOutput).invoke(prompt)
        return response.dict()

class ReviewerAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.system_prompt = """Ти - Reviewer. Твоє завдання: перевірити JSON, згенерований Extractor.
        Зістав JSON з оригінальним текстом. Шукай галюцинації (вигадані джерела) або пропущені маркери.
        Якщо є проблеми, встанови verdict 'repair_needed' та опишіть їх в issues. Якщо все ідеально - 'accept'."""

    def run(self, text: str, extracted_data: dict) -> dict:
        prompt = f"{self.system_prompt}\n\nОригінальний текст:\n{text}\n\nЗгенерований JSON:\n{json.dumps(extracted_data, ensure_ascii=False)}"
        response = self.llm.with_structured_output(ReviewerOutput).invoke(prompt)
        return response.dict()

class FallbackAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.system_prompt = """Ти - Repair/Fallback Agent. Твоє завдання: отримати сирий текст, 
        попередній JSON та список зауважень від Reviewer, і виправити помилки.
        Змінюй лише ті поля, на які вказав Reviewer."""

    def run(self, text: str, extracted_data: dict, issues: list) -> dict:
        prompt = f"{self.system_prompt}\n\nТекст:\n{text}\n\nПопередній JSON:\n{json.dumps(extracted_data, ensure_ascii=False)}\n\nПроблеми для виправлення:\n{json.dumps(issues, ensure_ascii=False)}"
        response = self.llm.with_structured_output(ExtractorOutput).invoke(prompt)
        return response.dict()