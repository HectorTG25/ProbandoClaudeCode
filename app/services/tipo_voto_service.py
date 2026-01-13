from typing import List, Optional, Dict, Any
from app.models import db, TipoVoto
from .base_service import BaseService

class TipoVotoService(BaseService):
    """Servicio para gestionar tipos de voto"""

    def __init__(self):
        super().__init__(TipoVoto)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los tipos de voto"""
        tipos = self.model.query.all()
        return [self._to_dict(tipo) for tipo in tipos]

    def get_by_id(self, id_tipo_voto: int) -> Optional[Dict[str, Any]]:
        """Obtiene un tipo de voto por su ID"""
        tipo = self.model.query.get(id_tipo_voto)
        return self._to_dict(tipo) if tipo else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo tipo de voto"""
        tipo = self.model(**data)
        db.session.add(tipo)
        db.session.commit()
        return self._to_dict(tipo)
