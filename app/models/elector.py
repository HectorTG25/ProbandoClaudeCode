from . import db

class Elector(db.Model):
    """Modelo que representa a un elector"""
    __tablename__ = 'elector'

    dni = db.Column(db.String(20), primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    distrito = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)

    votos = db.relationship('Voto', back_populates='elector', lazy=True)

    def to_dict(self):
        return {
            'dni': self.dni,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'distrito': self.distrito,
            'region': self.region
        }
