from typing import List, Optional, Dict, Any
from app.models import db, Elector
from .base_service import BaseService

class ElectorService(BaseService):
    """
    Servicio para gestionar electores.
    Implementa BaseService respetando LSP: puede sustituir a la clase base
    sin romper el contrato establecido.
    """

    def __init__(self):
        super().__init__(Elector)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los electores"""
        electores = self.model.query.all()
        return [self._to_dict(elector) for elector in electores]

    def get_by_id(self, dni: str) -> Optional[Dict[str, Any]]:
        """Obtiene un elector por su DNI"""
        elector = self.model.query.get(dni)
        return self._to_dict(elector) if elector else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo elector"""
        elector = self.model(**data)
        db.session.add(elector)
        db.session.commit()
        return self._to_dict(elector)
