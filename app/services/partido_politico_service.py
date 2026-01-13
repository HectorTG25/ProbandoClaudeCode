from typing import List, Optional, Dict, Any
from app.models import db, PartidoPolitico
from .base_service import BaseService

class PartidoPoliticoService(BaseService):
    """Servicio para gestionar partidos políticos"""

    def __init__(self):
        super().__init__(PartidoPolitico)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los partidos políticos"""
        partidos = self.model.query.all()
        return [self._to_dict(partido) for partido in partidos]

    def get_by_id(self, id_partido: int) -> Optional[Dict[str, Any]]:
        """Obtiene un partido político por su ID"""
        partido = self.model.query.get(id_partido)
        return self._to_dict(partido) if partido else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo partido político"""
        partido = self.model(**data)
        db.session.add(partido)
        db.session.commit()
        return self._to_dict(partido)
