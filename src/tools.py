import json

SOURCES_DB = {
    "гш зсу": "Офіційне, надійне джерело.",
    "міністерство оборони": "Офіційне, надійне джерело.",
    "риа новости": "Російська пропаганда, не довіряти.",
    "анонімний телеграм": "Низька надійність, можливі маніпуляції.",
    "труха": "Агрегатор, надійність середня."
}

FACTS_DB = {
    "мобілізація": "Жінок не мобілізують примусово. Студенти мають відстрочку.",
    "наступ з білорусі": "Ознак формування ударного угруповання немає.",
    "блекаут": "Відключення планові через атаки, тотальної евакуації не планується."
}

def check_source_credibility(source_name: str) -> str:
    source_lower = source_name.lower().strip()
    for key, value in SOURCES_DB.items():
        if key in source_lower:
            return value
    return "Джерело невідоме."

def get_official_fact(topic: str) -> str:
    topic_lower = topic.lower().strip()
    for key, value in FACTS_DB.items():
        if key in topic_lower:
            return value
    return "Офіційних даних не знайдено."

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "check_source_credibility",
            "description": "Перевірка надійності джерела новини",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"}
                },
                "required": ["source_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_official_fact",
            "description": "Пошук офіційних підтверджень або спростувань ключової теми",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"}
                },
                "required": ["topic"]
            }
        }
    }
]

available_tools = {
    "check_source_credibility": check_source_credibility,
    "get_official_fact": get_official_fact
}