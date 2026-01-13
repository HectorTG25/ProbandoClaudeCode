from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class BaseService(ABC):
    """
    Clase base abstracta para servicios.
    Aplicación del Principio de Sustitución de Liskov (LSP):
    - Define un contrato que todas las clases hijas deben cumplir
    - Las clases hijas pueden sustituir a la base sin romper la funcionalidad
    - No se fuerzan métodos que las clases hijas no puedan implementar correctamente
    """

    def __init__(self, model):
        """
        Constructor que recibe el modelo de SQLAlchemy
        :param model: Modelo de la entidad
        """
        self.model = model

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros
        :return: Lista de registros como diccionarios
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id: Any) -> Optional[Dict[str, Any]]:
        """
        Obtiene un registro por su ID
        :param entity_id: ID del registro
        :return: Registro como diccionario o None
        """
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo registro
        :param data: Datos del registro a crear
        :return: Registro creado como diccionario
        """
        pass

    def _to_dict(self, entity) -> Dict[str, Any]:
        """
        Convierte una entidad a diccionario
        :param entity: Entidad del modelo
        :return: Diccionario con los datos
        """
        if hasattr(entity, 'to_dict'):
            return entity.to_dict()
        return {}
