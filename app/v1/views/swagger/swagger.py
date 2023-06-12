import os
from flasgger import Swagger

template = {
    "swagger": "2.0",
    "info": {
        "title": "XYZ API Docs",
        "description": "API Documentation for XYZ Application",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "XYZ@XYZ.com",
            "url": "XYZ.com",
        },
        "termsOfService": "XYZ .com",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "\
            JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger_config = {
    "headers": [

        ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,

}


route = os.path.abspath(os.path.dirname(__file__))
print(route)