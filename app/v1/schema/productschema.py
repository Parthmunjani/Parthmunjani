product_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'name': {'type': 'string', 'maxLength': 50},
        'price': {'type': 'number', 'minimum': 0},
        'category_id': {'type': 'integer'},
        'created_at': {'type': 'string', 'format': 'date-time'},
        'modified_at': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['name', 'price', 'category_id'],
}
