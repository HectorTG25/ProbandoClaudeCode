from . import db

class Categoria(db.Model):
    """Modelo que representa una categoría de votación"""
    __tablename__ = 'categoria'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_categoria = db.Column(db.String(100), nullable=False, unique=True)
    ambito = db.Column(db.String(50), nullable=False)

    candidatos = db.relationship('Candidato', back_populates='categoria', lazy=True)
    voto_categorias = db.relationship('VotoCategoria', back_populates='categoria', lazy=True)

    def to_dict(self):
        return {
            'id_categoria': self.id_categoria,
            'nombre_categoria': self.nombre_categoria,
            'ambito': self.ambito
        }
