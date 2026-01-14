from . import db


class Respuesta(db.Model):
    """
    Modelo que representa una respuesta a una pregunta dentro de un cuestionario.
    Clave primaria compuesta: (id_cuestionario, id_pregunta)
    Garantiza que cada pregunta se responda una sola vez por cuestionario.
    """
    __tablename__ = 'respuesta'

    id_cuestionario = db.Column(
        db.Integer,
        db.ForeignKey('cuestionario.id_cuestionario'),
        primary_key=True
    )
    id_pregunta = db.Column(
        db.Integer,
        db.ForeignKey('pregunta.id_pregunta'),
        primary_key=True
    )
    id_opcion = db.Column(
        db.Integer,
        db.ForeignKey('opcion.id_opcion'),
        nullable=False
    )

    # Relaciones
    cuestionario = db.relationship('Cuestionario', back_populates='respuestas')
    pregunta = db.relationship('Pregunta', back_populates='respuestas')
    opcion = db.relationship('Opcion', back_populates='respuestas')

    def to_dict(self):
        return {
            'id_cuestionario': self.id_cuestionario,
            'id_pregunta': self.id_pregunta,
            'id_opcion': self.id_opcion
        }
