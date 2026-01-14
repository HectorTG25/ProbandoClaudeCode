from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelos del sistema de votación
from .elector import Elector
from .voto import Voto
from .tipo_voto import TipoVoto
from .partido_politico import PartidoPolitico
from .candidato import Candidato
from .categoria import Categoria
from .voto_categoria import VotoCategoria

# Modelos del módulo de cuestionario (independiente del sistema de votación)
from .cuestionario import Cuestionario
from .pregunta import Pregunta
from .opcion import Opcion
from .respuesta import Respuesta
