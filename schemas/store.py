create_store_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'user_id': {'type': 'string'},
    },
    'required': ['name', 'description', 'user_id']
}

update_store_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'user_id': {'type': 'string'},
        'is_active': {'type': 'boolean'}
    },
    'required': []
}
