from flask import Flask, send_from_directory
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

    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(config_by_name[config_name])

    # Inicializar extensiones
    db.init_app(app)
    CORS(app)  # Habilitar CORS para todas las rutas
    Swagger(app, template=swagger_template, config=swagger_config)

    # Registrar blueprints del sistema de votación
    from app.controllers import (
        elector_bp, voto_bp, tipo_voto_bp,
        partido_politico_bp, candidato_bp,
        categoria_bp, voto_categoria_bp,
        # Blueprints del módulo de cuestionario
        pregunta_bp, cuestionario_bp
    )

    app.register_blueprint(elector_bp)
    app.register_blueprint(voto_bp)
    app.register_blueprint(tipo_voto_bp)
    app.register_blueprint(partido_politico_bp)
    app.register_blueprint(candidato_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(voto_categoria_bp)

    # Blueprints del módulo de cuestionario (independiente)
    app.register_blueprint(pregunta_bp)
    app.register_blueprint(cuestionario_bp)

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/cedula')
    def cedula():
        return send_from_directory(app.static_folder, 'index.html')

    # Ruta para servir archivos estáticos
    @app.route('/<path:path>')
    def static_files(path):
        return send_from_directory(app.static_folder, path)

    return app
