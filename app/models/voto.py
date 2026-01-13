from . import db
from datetime import datetime

class Voto(db.Model):
    """Modelo que representa un voto"""
    __tablename__ = 'voto'

    id_voto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dni = db.Column(db.String(20), db.ForeignKey('elector.dni'), nullable=False)
    id_tipo_voto = db.Column(db.Integer, db.ForeignKey('tipo_voto.id_tipo_voto'), nullable=False)

    elector = db.relationship('Elector', back_populates='votos')
    tipo_voto = db.relationship('TipoVoto', back_populates='votos')
    voto_categorias = db.relationship('VotoCategoria', back_populates='voto', lazy=True)

    def to_dict(self):
        return {
            'id_voto': self.id_voto,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'dni': self.dni,
            'id_tipo_voto': self.id_tipo_voto
        }
