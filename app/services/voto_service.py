from typing import List, Optional, Dict, Any
from app.models import db, Voto, VotoCategoria, TipoVoto, Categoria
from .base_service import BaseService
from sqlalchemy.exc import IntegrityError

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

    def dni_ya_voto(self, dni: str) -> bool:
        """Verifica si un DNI ya ha votado"""
        voto = self.model.query.filter_by(dni=dni).first()
        return voto is not None

    def determinar_tipo_voto(self, votos_categoria_data: List[Dict[str, Any]]) -> int:
        """
        Determina el tipo de voto basado en las categorías:
        - Si todas las categorías están en blanco (sin id_partido) -> Voto en blanco (id=3)
        - Si hay al menos una categoría con partido -> Voto válido (id=1)
        """
        # Obtener tipos de voto
        tipo_valido = TipoVoto.query.filter_by(nombre_tipo='Válido').first()
        tipo_blanco = TipoVoto.query.filter_by(nombre_tipo='En Blanco').first()

        if not tipo_valido or not tipo_blanco:
            raise ValueError('Los tipos de voto "Válido" y "En Blanco" deben existir en la tabla TIPO_VOTO')

        # Si no hay votos por categoría o todos tienen id_partido=None, es voto en blanco
        if not votos_categoria_data:
            return tipo_blanco.id_tipo_voto

        tiene_voto_valido = any(vc.get('id_partido') is not None for vc in votos_categoria_data)

        return tipo_valido.id_tipo_voto if tiene_voto_valido else tipo_blanco.id_tipo_voto

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo voto con sus respectivos votos por categoría.

        Maneja:
        1. Validación de DNI duplicado
        2. Votos en blanco (todas las categorías sin partido)
        3. Determinación automática del tipo de voto

        Espera data con formato:
        {
            "dni": "12345678",
            "votos_categoria": [
                {
                    "id_categoria": 1,
                    "id_partido": 1,  # NULL para voto en blanco
                    "numero_preferencial_1": 101,
                    "numero_preferencial_2": 102
                }
            ]
        }
        """
        dni = data.get('dni')

        # Validar que el DNI no haya votado ya
        if self.dni_ya_voto(dni):
            raise ValueError(f'El DNI {dni} ya ha registrado un voto. No puede votar nuevamente.')

        # Extraer votos por categoría
        votos_categoria_data = data.pop('votos_categoria', [])

        # Determinar automáticamente el tipo de voto
        id_tipo_voto = self.determinar_tipo_voto(votos_categoria_data)

        # Si no se proporcionaron votos por categoría, crear uno por cada categoría en blanco
        if not votos_categoria_data:
            categorias = Categoria.query.all()
            votos_categoria_data = [
                {
                    'id_categoria': cat.id_categoria,
                    'id_partido': None,
                    'numero_preferencial_1': None,
                    'numero_preferencial_2': None
                }
                for cat in categorias
            ]

        # Crear el voto principal
        voto = self.model(
            dni=dni,
            id_tipo_voto=id_tipo_voto
        )
        db.session.add(voto)

        try:
            db.session.flush()  # Para obtener el id_voto antes del commit

            # Crear votos por categoría asociados
            for vc_data in votos_categoria_data:
                voto_categoria = VotoCategoria(
                    id_voto=voto.id_voto,
                    id_categoria=vc_data.get('id_categoria'),
                    id_partido=vc_data.get('id_partido'),  # Puede ser NULL para voto en blanco
                    numero_preferencial_1=vc_data.get('numero_preferencial_1'),
                    numero_preferencial_2=vc_data.get('numero_preferencial_2')
                )
                db.session.add(voto_categoria)

            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            if 'unique constraint' in str(e).lower() or 'duplicate' in str(e).lower():
                raise ValueError(f'El DNI {dni} ya ha registrado un voto. No puede votar nuevamente.')
            raise

        # Retornar con votos por categoría incluidos
        voto_dict = self._to_dict(voto)
        voto_dict['votos_categoria'] = [
            vc.to_dict() for vc in voto.voto_categorias
        ]
        return voto_dict
