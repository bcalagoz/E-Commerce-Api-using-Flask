order_schema = {
    "type": "object",
    "properties": {
        "customer_id": {"type": "string"},
        "shop_id": {"type": "string"},
        "total_price": {"type": "string"},
        "status": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "quantity": {"type": "string"},
                    "price": {"type": "string"}
                },
                "required": ["product_id", "quantity", "price"]
            }
        }
    },
    "required": ["customer_id", "shop_id", "total_price", "status", "items"]
}