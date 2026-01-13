from typing import List, Optional, Dict, Any
from app.models import db, Categoria
from .base_service import BaseService

class CategoriaService(BaseService):
    """Servicio para gestionar categorías de votación"""

    def __init__(self):
        super().__init__(Categoria)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las categorías"""
        categorias = self.model.query.all()
        return [self._to_dict(categoria) for categoria in categorias]

    def get_by_id(self, id_categoria: int) -> Optional[Dict[str, Any]]:
        """Obtiene una categoría por su ID"""
        categoria = self.model.query.get(id_categoria)
        return self._to_dict(categoria) if categoria else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva categoría"""
        categoria = self.model(**data)
        db.session.add(categoria)
        db.session.commit()
        return self._to_dict(categoria)
