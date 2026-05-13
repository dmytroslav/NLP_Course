import json

class EvalAgent:
    """
    Агент-оцінювач (LLM-as-a-Judge) для перевірки правильності 
    фінальних вердиктів FactCheck агента.
    """
    def __init__(self, client, model="llama-3.1-8b-instant"):
        self.client = client
        self.model = model
        self.system_prompt = """Ти — незалежний суддя. 
Твоя задача — оцінити, чи правильний вердикт виніс FactCheck Agent.
Доступні оцінки:
- correct (вердикт повністю збігається з очікуваним)
- partly correct (агент заплутався, або не зміг винести точний вердикт через неоднозначність)
- wrong (агент видав протилежний результат)

ВИДАЙ ТІЛЬКИ ОДНЕ З ЦИХ ТРЬОХ ЗНАЧЕНЬ БЕЗ ЖОДНИХ ПОЯСНЕНЬ."""

    def evaluate(self, news_text: str, actual_verdict: str, expected_verdict: str) -> str:
        prompt = f"""
Новина: {news_text}
Очікуваний вердикт: {expected_verdict}
Фактичний вердикт агента: {actual_verdict}

Оцінка:"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            return f"error: {str(e)}"