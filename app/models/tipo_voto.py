from . import db

class TipoVoto(db.Model):
    """Modelo que representa un tipo de voto"""
    __tablename__ = 'tipo_voto'

    id_tipo_voto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_tipo = db.Column(db.String(50), nullable=False, unique=True)

    votos = db.relationship('Voto', back_populates='tipo_voto', lazy=True)

    def to_dict(self):
        return {
            'id_tipo_voto': self.id_tipo_voto,
            'nombre_tipo': self.nombre_tipo
        }
