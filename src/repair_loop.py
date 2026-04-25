from src.llm_extract import client, get_baseline_prompt
from src.validator import validate_json

def extract_with_repair(text, schema, max_attempts=2, model="llama-3.1-8b-instant"):
    prompt = get_baseline_prompt(text)
    
    for attempt in range(max_attempts + 1):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0.0
            )
            raw_output = response.choices[0].message.content.strip()
            
            is_valid, parsed_json, error_msg = validate_json(raw_output, schema)
            
            if is_valid:
                return {
                    "final_json": parsed_json,
                    "status": "success",
                    "attempts": attempt + 1,
                    "error": None
                }
            
            if attempt < max_attempts:
                prompt = f"""Ти повернув невалідний результат.
Попередній вивід:
{raw_output}

Помилка валідації:
{error_msg}

Виправ помилку і поверни ТІЛЬКИ валідний JSON, що відповідає схемі. Жодного тексту.
Текст: "{text}"
JSON:"""
            else:
                return {
                    "final_json": parsed_json, 
                    "status": "failed",
                    "attempts": attempt + 1,
                    "error": error_msg,
                    "raw_output": raw_output
                }
                
        except Exception as e:
            return {
                "final_json": None,
                "status": "api_error",
                "attempts": attempt + 1,
                "error": str(e)
            }