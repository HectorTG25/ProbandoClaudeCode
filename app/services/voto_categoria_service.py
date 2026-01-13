from typing import List, Optional, Dict, Any
from app.models import db, VotoCategoria
from .base_service import BaseService

class VotoCategoriaService(BaseService):
    """Servicio para gestionar votos por categoría"""

    def __init__(self):
        super().__init__(VotoCategoria)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los votos por categoría"""
        votos_categoria = self.model.query.all()
        return [self._to_dict(voto_cat) for voto_cat in votos_categoria]

    def get_by_id(self, id_voto_categoria: int) -> Optional[Dict[str, Any]]:
        """Obtiene un voto por categoría por su ID"""
        voto_cat = self.model.query.get(id_voto_categoria)
        return self._to_dict(voto_cat) if voto_cat else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo voto por categoría"""
        voto_cat = self.model(**data)
        db.session.add(voto_cat)
        db.session.commit()
        return self._to_dict(voto_cat)
