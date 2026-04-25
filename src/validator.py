import json
from jsonschema import validate, ValidationError

def validate_json(json_str, schema):
    try:
        parsed_json = json.loads(json_str)
    except json.JSONDecodeError as e:
        return False, None, f"JSON Parse Error: {str(e)}"
    
    try:
        validate(instance=parsed_json, schema=schema)
        return True, parsed_json, "Valid"
    except ValidationError as e:
        return False, parsed_json, f"Schema Error: {e.message}"