from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config.config import config_by_name
from app.models import db
from app.swagger import swagger_template, swagger_config
import os

def create_app(config_name=None):
    """Factory para crear la aplicación Flask"""

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Inicializar extensiones
    db.init_app(app)
    CORS(app)
    Swagger(app, template=swagger_template, config=swagger_config)

    # Registrar blueprints
    from app.controllers import (
        elector_bp, voto_bp, tipo_voto_bp,
        partido_politico_bp, candidato_bp,
        categoria_bp, voto_categoria_bp
    )

    app.register_blueprint(elector_bp)
    app.register_blueprint(voto_bp)
    app.register_blueprint(tipo_voto_bp)
    app.register_blueprint(partido_politico_bp)
    app.register_blueprint(candidato_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(voto_categoria_bp)

    @app.route('/')
    def index():
        return {
            'mensaje': 'API de Votación',
            'documentacion': '/api/docs',
            'version': '1.0.0'
        }

    return app
