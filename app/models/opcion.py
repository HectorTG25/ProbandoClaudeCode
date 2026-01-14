from . import db


class Opcion(db.Model):
    """
    Modelo que representa una opción de respuesta para una pregunta.
    """
    __tablename__ = 'opcion'

    id_opcion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('pregunta.id_pregunta'), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    es_correcta = db.Column(db.Boolean, nullable=False, default=False)

    # Relación con pregunta
    pregunta = db.relationship('Pregunta', back_populates='opciones')
    # Relación con respuestas
    respuestas = db.relationship('Respuesta', back_populates='opcion', lazy=True)

    def to_dict(self):
        """Diccionario completo (uso interno/administrativo)"""
        return {
            'id_opcion': self.id_opcion,
            'id_pregunta': self.id_pregunta,
            'texto': self.texto,
            'es_correcta': self.es_correcta
        }

    def to_dict_publica(self):
        """Diccionario público (NO expone es_correcta)"""
        return {
            'id_opcion': self.id_opcion,
            'id_pregunta': self.id_pregunta,
            'texto': self.texto
        }
