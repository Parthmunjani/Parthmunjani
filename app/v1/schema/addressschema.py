user_address_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "integer"},
        "street": {"type": "string", "maxLength": 200},
        "state": {"type": "string", "maxLength": 50},
        "zip": {"type": "integer", "minimum": 4, "maximum": 7}
    },
    "required": ["user_id", "street", "state", "zip"]
}

