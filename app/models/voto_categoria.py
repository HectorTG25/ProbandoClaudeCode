from . import db

class VotoCategoria(db.Model):
    """Modelo que representa el voto por categoría con votos preferenciales"""
    __tablename__ = 'voto_categoria'

    id_voto_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_voto = db.Column(db.Integer, db.ForeignKey('voto.id_voto'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    id_partido = db.Column(db.Integer, db.ForeignKey('partido_politico.id_partido'), nullable=True)  # NULL para votos en blanco
    numero_preferencial_1 = db.Column(db.Integer, nullable=True)  # NULL si no hay preferencial
    numero_preferencial_2 = db.Column(db.Integer, nullable=True)  # NULL si no hay preferencial

    voto = db.relationship('Voto', back_populates='voto_categorias')
    categoria = db.relationship('Categoria', back_populates='voto_categorias')
    partido = db.relationship('PartidoPolitico', back_populates='voto_categorias')

    def to_dict(self):
        return {
            'id_voto_categoria': self.id_voto_categoria,
            'id_voto': self.id_voto,
            'id_categoria': self.id_categoria,
            'id_partido': self.id_partido,
            'numero_preferencial_1': self.numero_preferencial_1,
            'numero_preferencial_2': self.numero_preferencial_2
        }
