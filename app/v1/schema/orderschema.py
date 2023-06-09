order_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'user_id': {'type': 'integer'},
        'payment_status': {'type': 'string'},
        'address_id': {'type': 'integer'},
        'category_id': {'type': 'integer'},
        'total_price': {'type': 'number'},
        'status': {'type': 'string'},
        'created_at': {'type': 'string', 'format': 'date-time'},
        'modified_at': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['user_id', 'payment_status', 'address_id', 'category_id', 'total_price', 'status'],
}