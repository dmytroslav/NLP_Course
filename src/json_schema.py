event_schema = {
    "type": "object",
    "properties": {
        "event_type": {
            "type": "string",
            "enum": ["missile_strike", "drone_attack", "ground_combat", "diplomacy", "other"]
        },
        "location": {
            "type": ["string", "null"]
        },
        "weapons": {
            "type": "array",
            "items": {"type": "string"}
        },
        "casualties": {
            "type": ["string", "null"]
        },
        "date_text": {
            "type": ["string", "null"]
        }
    },
    "required": ["event_type", "location", "weapons"],
    "additionalProperties": False
}