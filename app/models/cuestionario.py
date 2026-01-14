from . import db
from datetime import datetime


class Cuestionario(db.Model):
    """
    Modelo que representa un cuestionario completado.
    Completamente independiente del sistema de votación.
    No almacena datos personales para mantener el anonimato.
    """
    __tablename__ = 'cuestionario'

    id_cuestionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relación con respuestas
    respuestas = db.relationship('Respuesta', back_populates='cuestionario', lazy=True)

    def to_dict(self):
        return {
            'id_cuestionario': self.id_cuestionario,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
