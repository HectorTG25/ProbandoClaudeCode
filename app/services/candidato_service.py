from typing import List, Optional, Dict, Any
from app.models import db, Candidato
from .base_service import BaseService

class CandidatoService(BaseService):
    """Servicio para gestionar candidatos"""

    def __init__(self):
        super().__init__(Candidato)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los candidatos"""
        candidatos = self.model.query.all()
        return [self._to_dict(candidato) for candidato in candidatos]

    def get_by_id(self, id_candidato: int) -> Optional[Dict[str, Any]]:
        """Obtiene un candidato por su ID"""
        candidato = self.model.query.get(id_candidato)
        return self._to_dict(candidato) if candidato else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo candidato"""
        candidato = self.model(**data)
        db.session.add(candidato)
        db.session.commit()
        return self._to_dict(candidato)
