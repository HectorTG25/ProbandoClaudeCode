from typing import List, Dict, Any, Optional
from app.models import db, Cuestionario, Respuesta, Pregunta, Opcion
from .base_service import BaseService


class CuestionarioService(BaseService):
    """
    Servicio para gestionar cuestionarios de conocimiento ciudadano.
    Implementa BaseService respetando LSP.

    RESTRICCIONES ÉTICAS:
    - No almacena DNI, id_voto, IP ni datos identificables
    - Completamente independiente del sistema de votación
    - No proporciona feedback sobre respuestas correctas
    """

    def __init__(self):
        super().__init__(Cuestionario)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los cuestionarios"""
        cuestionarios = self.model.query.all()
        return [self._to_dict(c) for c in cuestionarios]

    def get_by_id(self, cuestionario_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un cuestionario por ID"""
        cuestionario = self.model.query.get(cuestionario_id)
        return self._to_dict(cuestionario) if cuestionario else None

    def get_by_id_con_respuestas(self, cuestionario_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un cuestionario con sus respuestas (sin indicar correctas)"""
        cuestionario = self.model.query.get(cuestionario_id)
        if not cuestionario:
            return None

        return {
            'id_cuestionario': cuestionario.id_cuestionario,
            'fecha': cuestionario.fecha.isoformat() if cuestionario.fecha else None,
            'respuestas': [r.to_dict() for r in cuestionario.respuestas]
        }

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo cuestionario con sus respuestas.

        Formato esperado:
        {
            "respuestas": [
                {"id_pregunta": 1, "id_opcion": 3},
                {"id_pregunta": 2, "id_opcion": 7},
                ...
            ]
        }
        """
        # Validar que hay respuestas
        respuestas_data = data.get('respuestas', [])
        if not respuestas_data:
            raise ValueError('Debe proporcionar al menos una respuesta')

        # Validar referencias
        for resp in respuestas_data:
            id_pregunta = resp.get('id_pregunta')
            id_opcion = resp.get('id_opcion')

            if not id_pregunta or not id_opcion:
                raise ValueError('Cada respuesta debe tener id_pregunta e id_opcion')

            # Verificar que la pregunta existe
            pregunta = Pregunta.query.get(id_pregunta)
            if not pregunta:
                raise ValueError(f'La pregunta con ID {id_pregunta} no existe')

            # Verificar que la opción existe
            opcion = Opcion.query.get(id_opcion)
            if not opcion:
                raise ValueError(f'La opción con ID {id_opcion} no existe')

            # Verificar que la opción pertenece a la pregunta
            if opcion.id_pregunta != id_pregunta:
                raise ValueError(
                    f'La opción {id_opcion} no pertenece a la pregunta {id_pregunta}'
                )

        # Crear cuestionario
        cuestionario = Cuestionario()
        db.session.add(cuestionario)
        db.session.flush()  # Obtener ID antes de crear respuestas

        # Crear respuestas
        for resp in respuestas_data:
            respuesta = Respuesta(
                id_cuestionario=cuestionario.id_cuestionario,
                id_pregunta=resp['id_pregunta'],
                id_opcion=resp['id_opcion']
            )
            db.session.add(respuesta)

        db.session.commit()

        return {
            'id_cuestionario': cuestionario.id_cuestionario,
            'fecha': cuestionario.fecha.isoformat(),
            'total_respuestas': len(respuestas_data),
            'mensaje': 'Cuestionario registrado exitosamente'
        }

    def contar_cuestionarios(self) -> int:
        """Retorna el total de cuestionarios completados (estadística)"""
        return self.model.query.count()


cuestionario_service = CuestionarioService()
