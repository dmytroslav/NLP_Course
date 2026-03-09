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
    # Шукаємо формати DD.MM.YYYY
    pattern = r'\b(\d{2})\.(\d{2})\.(\d{4})\b'
    results = []
    for match in re.finditer(pattern, text):
        raw_val = match.group(0)
        norm_val = f"{match.group(3)}-{match.group(2)}-{match.group(1)}" # Нормалізація YYYY-MM-DD
        results.append({
            "field_type": "DATE",
            "value": norm_val,
            "raw_value": raw_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "regex_dd_mm_yyyy"
        })
    return results

def extract_amounts(text: str) -> list[dict]:
    # Шукаємо суми (напр., "100 тис грн", "50 млн доларів")
    pattern = r'\b(\d+[.,]?\d*)\s*(тис|млн|млрд)?\.?\s*(грн|гривень|дол|доларів|євро|\$|₴)\b'
    results = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        raw_val = match.group(0)
        num_part = match.group(1).replace(',', '.')
        multiplier = match.group(2)
        curr_raw = match.group(3).lower()
        
        # Нормалізація валюти
        norm_curr = CURRENCIES_DICT.get(curr_raw, "UNKNOWN")
        
        results.append({
            "field_type": "AMOUNT",
            "value": f"{num_part} {multiplier if multiplier else ''} {norm_curr}".strip(),
            "raw_value": raw_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "regex_amount_with_currency"
        })
    return results

def extract_locations(text: str) -> list[dict]:
    results = []
    for loc in LOCATIONS_DICT:
        # Шукаємо точний збіг слова
        pattern = rf'\b{loc}\b'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            results.append({
                "field_type": "LOCATION",
                "value": loc, # Нормалізовано до словника
                "raw_value": match.group(0),
                "start_char": match.start(),
                "end_char": match.end(),
                "method": "dict_locations_ua"
            })
    return results

def extract_all(text: str) -> list[dict]:
    return extract_dates(text) + extract_amounts(text) + extract_locations(text)