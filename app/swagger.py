swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Votación",
        "description": "API REST para sistema de votación electrónica",
        "version": "1.0.0",
        "contact": {
            "name": "Sistema de Votación"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}
