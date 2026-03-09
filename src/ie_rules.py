import re
import json
import os

# Завантаження словників
def load_resources():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    locations_path = os.path.join(base_dir, 'resources', 'locations_ua.txt')
    currencies_path = os.path.join(base_dir, 'resources', 'currencies.json')
    
    with open(locations_path, 'r', encoding='utf-8') as f:
        locations = [line.strip() for line in f if line.strip()]
        
    with open(currencies_path, 'r', encoding='utf-8') as f:
        currencies = json.load(f)
        
    return locations, currencies

LOCATIONS_DICT, CURRENCIES_DICT = load_resources()

def extract_dates(text: str) -> list[dict]:
    # Оновлено: шукаємо формати DD.MM.YYYY та DD.MM.YY
    pattern = r'\b(\d{2})\.(\d{2})\.(\d{2,4})\b'
    results = []
    for match in re.finditer(pattern, text):
        raw_val = match.group(0)
        year = match.group(3)
        if len(year) == 2:
            year = "20" + year # Проста нормалізація для 2020-х
        norm_val = f"{year}-{match.group(2)}-{match.group(1)}"
        results.append({
            "field_type": "DATE",
            "value": norm_val,
            "raw_value": raw_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "regex_date_extended"
        })
    return results

def extract_amounts(text: str) -> list[dict]:
    # Анти-правило: (?!\s*/\s*[а-яa-z]+) відсікає те, що йде після слешу (наприклад, /л, /кг)
    pattern = r'\b(\d+[.,]?\d*)\s*(тис|млн|млрд)?\.?\s*(грн|гривень|дол|доларів|євро|\$|₴)\b(?!\s*/\s*[а-яa-z]+)'
    results = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        raw_val = match.group(0)
        num_part = match.group(1).replace(',', '.')
        multiplier = match.group(2)
        curr_raw = match.group(3).lower()
        
        norm_curr = CURRENCIES_DICT.get(curr_raw, "UNKNOWN")
        
        results.append({
            "field_type": "AMOUNT",
            "value": f"{num_part} {multiplier if multiplier else ''} {norm_curr}".strip().replace("  ", " "),
            "raw_value": raw_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "regex_amount_no_rates"
        })
    return results

def extract_locations(text: str) -> list[dict]:
    results = []
    for loc in LOCATIONS_DICT:
        # Анти-правило: (?<!Потяг \S{0,10} ) та (?<!трасі ) щоб відсікти маршрути
        pattern = rf'(?<!Потяг )\b{loc}\b(?! -)'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Проста перевірка контексту
            context_before = text[max(0, match.start()-15):match.start()].lower()
            if "трас" in context_before or "маршрут" in context_before or "потяг" in context_before:
                continue
                
            results.append({
                "field_type": "LOCATION",
                "value": loc,
                "raw_value": match.group(0),
                "start_char": match.start(),
                "end_char": match.end(),
                "method": "dict_locations_filtered"
            })
    return results

def extract_all(text: str) -> list[dict]:
    return extract_dates(text) + extract_amounts(text) + extract_locations(text)