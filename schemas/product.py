product_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'price': {'type': 'string'},
        'image_url': {'type': 'string'},
        'shop_id': {'type': 'string'},
    },
    'required': ['name', 'description', 'price', 'image_url', 'shop_id']
}
