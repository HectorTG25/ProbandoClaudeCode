from . import db

class Candidato(db.Model):
    """Modelo que representa un candidato"""
    __tablename__ = 'candidato'

    id_candidato = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_candidato = db.Column(db.String(100), nullable=False)
    numero_candidato = db.Column(db.Integer, nullable=True)  # Nullable para presidente y vicepresidente
    id_partido = db.Column(db.Integer, db.ForeignKey('partido_politico.id_partido'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)

    partido = db.relationship('PartidoPolitico', back_populates='candidatos')
    categoria = db.relationship('Categoria', back_populates='candidatos')

    def to_dict(self):
        return {
            'id_candidato': self.id_candidato,
            'nombre_candidato': self.nombre_candidato,
            'numero_candidato': self.numero_candidato,
            'id_partido': self.id_partido,
            'id_categoria': self.id_categoria
        }
