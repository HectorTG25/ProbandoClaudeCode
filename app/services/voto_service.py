from typing import List, Optional, Dict, Any
from app.models import db, Voto, VotoCategoria
from .base_service import BaseService

class VotoService(BaseService):
    """Servicio para gestionar votos"""

    def __init__(self):
        super().__init__(Voto)

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los votos"""
        votos = self.model.query.all()
        return [self._to_dict(voto) for voto in votos]

    def get_by_id(self, id_voto: int) -> Optional[Dict[str, Any]]:
        """Obtiene un voto por su ID con sus votos por categoría"""
        voto = self.model.query.get(id_voto)
        if not voto:
            return None

        voto_dict = self._to_dict(voto)
        # Incluir votos por categoría
        voto_dict['votos_categoria'] = [
            vc.to_dict() for vc in voto.voto_categorias
        ]
        return voto_dict

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo voto con sus respectivos votos por categoría.

        Espera data con formato:
        {
            "dni": "12345678",
            "id_tipo_voto": 1,
            "votos_categoria": [
                {
                    "id_categoria": 1,
                    "id_partido": 1,
                    "numero_preferencial_1": 101,
                    "numero_preferencial_2": 102
                }
            ]
        }
        """
        # Extraer votos por categoría si existen
        votos_categoria_data = data.pop('votos_categoria', [])

        # Crear el voto principal
        voto = self.model(**data)
        db.session.add(voto)
        db.session.flush()  # Para obtener el id_voto antes del commit

        # Crear votos por categoría asociados
        for vc_data in votos_categoria_data:
            voto_categoria = VotoCategoria(
                id_voto=voto.id_voto,
                id_categoria=vc_data.get('id_categoria'),
                id_partido=vc_data.get('id_partido'),
                numero_preferencial_1=vc_data.get('numero_preferencial_1'),
                numero_preferencial_2=vc_data.get('numero_preferencial_2')
            )
            db.session.add(voto_categoria)

        db.session.commit()

        # Retornar con votos por categoría incluidos
        voto_dict = self._to_dict(voto)
        voto_dict['votos_categoria'] = [
            vc.to_dict() for vc in voto.voto_categorias
        ]
        return voto_dict
