import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Obtener DATABASE_URL o construirla desde componentes individuales
    database_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')

    if not database_url:
        # Si no existe DATABASE_URL, construirla desde componentes
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'voting_db')

        # Codificar contraseña para manejar caracteres especiales
        encoded_password = quote_plus(db_password)
        database_url = f'postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}'

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
