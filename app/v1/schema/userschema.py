user_schema={
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'uuid': {'type': 'string', 'format': 'uuid'},
        'name': {'type': 'string', 'maxLength': 255},
        'email': {'type': 'string', 'format': 'email', 'maxLength': 255},
        'password': {'type': 'string', 'maxLength': 255},
        'phone_number': {'type': 'string', 'maxLength': 20},
        'id_proof_document': {'type': 'string', 'contentEncoding': 'base64'},
        'created_at': {'type': 'string', 'format': 'date-time'},
        'modified_at': {'type': 'string', 'format': 'date-time'},
        'is_deleted': {'type': 'boolean'}
    },
    'required': ['name', 'email', 'phone_number', 'password']
}

"""@staticmethod
    def validate(data):
        try:
            jsonschema.validate(data, UserSchema.user_model_schema)
            return True
        except jsonschema.ValidationError:
            return False"""