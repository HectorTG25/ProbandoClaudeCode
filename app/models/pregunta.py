from . import db


class Pregunta(db.Model):
    """
    Modelo que representa una pregunta del cuestionario de conocimiento ciudadano.
    """
    __tablename__ = 'pregunta'

    id_pregunta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.String(500), nullable=False)

    # Relación con opciones
    opciones = db.relationship('Opcion', back_populates='pregunta', lazy=True)
    # Relación con respuestas
    respuestas = db.relationship('Respuesta', back_populates='pregunta', lazy=True)

    def to_dict(self):
        """Diccionario básico sin opciones"""
        return {
            'id_pregunta': self.id_pregunta,
            'texto': self.texto
        }

    def to_dict_con_opciones(self):
        """Diccionario con opciones (sin exponer es_correcta)"""
        return {
            'id_pregunta': self.id_pregunta,
            'texto': self.texto,
            'opciones': [opcion.to_dict_publica() for opcion in self.opciones]
        }
