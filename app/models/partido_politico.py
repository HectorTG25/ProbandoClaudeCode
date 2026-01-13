from . import db

class PartidoPolitico(db.Model):
    """Modelo que representa un partido político"""
    __tablename__ = 'partido_politico'

    id_partido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_partido = db.Column(db.String(100), nullable=False, unique=True)
    logo = db.Column(db.String(255))

    candidatos = db.relationship('Candidato', back_populates='partido', lazy=True)
    voto_categorias = db.relationship('VotoCategoria', back_populates='partido', lazy=True)

    def to_dict(self):
        return {
            'id_partido': self.id_partido,
            'nombre_partido': self.nombre_partido,
            'logo': self.logo
        }
