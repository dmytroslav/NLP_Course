import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY", "GROQ_API")
client = Groq(api_key=api_key)

def get_baseline_prompt(text):
    return f"""Ти — AI-асистент для аналізу військових новин.
Твоє завдання: витягнути інформацію з тексту і повернути її ТІЛЬКИ у форматі валідного JSON.
Не пиши жодних пояснень, вступних слів або форматування markdown (без ```json).

Структура JSON має бути точно такою:
- event_type: рядок, суворо одне з значень: ["missile_strike", "drone_attack", "ground_combat", "diplomacy", "other"]
- location: рядок (місто, регіон) або null, якщо не вказано
- weapons: масив рядків (назви зброї, техніки). Якщо немає - порожній масив []
- casualties: рядок (інформація про жертви/постраждалих) або null, якщо не вказано
- date_text: рядок або null

Текст: "{text}"
JSON:"""

def extract_raw(text, model="llama-3.1-8b-instant"):
    prompt = get_baseline_prompt(text)
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.0 
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)