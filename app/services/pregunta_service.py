from typing import List, Dict, Any, Optional
from app.models import db, Pregunta
from .base_service import BaseService


class PreguntaService(BaseService):
    """
    Servicio para gestionar preguntas del cuestionario.
    Implementa BaseService respetando LSP.
    """

    def __init__(self):
        super().__init__(Pregunta)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las preguntas (sin opciones)"""
        preguntas = self.model.query.all()
        return [self._to_dict(p) for p in preguntas]

    def get_all_con_opciones(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las preguntas con sus opciones.
        NO expone el campo es_correcta por motivos éticos.
        """
        preguntas = self.model.query.all()
        return [p.to_dict_con_opciones() for p in preguntas]

    def get_by_id(self, pregunta_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una pregunta por ID"""
        pregunta = self.model.query.get(pregunta_id)
        return self._to_dict(pregunta) if pregunta else None

    def get_by_id_con_opciones(self, pregunta_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una pregunta con opciones por ID (sin es_correcta)"""
        pregunta = self.model.query.get(pregunta_id)
        return pregunta.to_dict_con_opciones() if pregunta else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva pregunta"""
        pregunta = Pregunta(texto=data['texto'])
        db.session.add(pregunta)
        db.session.commit()
        return self._to_dict(pregunta)


pregunta_service = PreguntaService()
