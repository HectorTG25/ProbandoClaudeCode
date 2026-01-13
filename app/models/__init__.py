from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .elector import Elector
from .voto import Voto
from .tipo_voto import TipoVoto
from .partido_politico import PartidoPolitico
from .candidato import Candidato
from .categoria import Categoria
from .voto_categoria import VotoCategoria
