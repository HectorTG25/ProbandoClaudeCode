# Aplicación de Principios SOLID en la API de Votación

Este documento explica cómo se han aplicado los principios SOLID en el diseño de la API.

## 1. Single Responsibility Principle (SRP)

**Cada clase tiene una única responsabilidad**

### Ejemplos:

- **Modelos** ([app/models/](app/models/)): Solo se encargan de definir la estructura de datos y relaciones de la base de datos
  - `Elector`: Define estructura del elector
  - `Voto`: Define estructura del voto
  - `PartidoPolitico`: Define estructura del partido

- **Servicios** ([app/services/](app/services/)): Contienen únicamente la lógica de negocio
  - `ElectorService`: Gestiona operaciones de electores
  - `VotoService`: Gestiona operaciones de votos
  - No mezclan lógica de presentación ni acceso directo a BD

- **Controllers** ([app/controllers/](app/controllers/)): Solo manejan peticiones HTTP y respuestas
  - `elector_controller.py`: Maneja endpoints de electores
  - `voto_controller.py`: Maneja endpoints de votos
  - No contienen lógica de negocio

## 2. Open/Closed Principle (OCP)

**El sistema está abierto para extensión pero cerrado para modificación**

### Ejemplos:

- **BaseService** ([app/services/base_service.py](app/services/base_service.py:1)): Define una estructura que puede extenderse
  - Nuevos servicios pueden heredar sin modificar el código base
  - Se pueden agregar nuevos métodos en las clases hijas sin afectar la clase base

- **Blueprints de Flask**: Nuevos endpoints se agregan registrando blueprints
  - No es necesario modificar el código existente para agregar nuevas rutas
  - Ejemplo en [app/__init__.py](app/__init__.py:28-35)

## 3. Liskov Substitution Principle (LSP)

**Las clases derivadas pueden sustituir a sus clases base sin romper la funcionalidad**

### Implementación Explícita:

#### Clase Base Abstracta: `BaseService`

```python
# app/services/base_service.py
class BaseService(ABC):
    """
    Define un contrato claro que todas las subclases deben cumplir
    """

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Todas las subclases DEBEN implementar este método"""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: Any) -> Optional[Dict[str, Any]]:
        """Todas las subclases DEBEN implementar este método"""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Todas las subclases DEBEN implementar este método"""
        pass
```

#### Clases Derivadas:

Todos los servicios implementan el contrato completo:

- [ElectorService](app/services/elector_service.py:9-28)
- [VotoService](app/services/voto_service.py:9-28)
- [PartidoPoliticoService](app/services/partido_politico_service.py:9-28)
- [CandidatoService](app/services/candidato_service.py:9-28)
- [CategoriaService](app/services/categoria_service.py:9-28)

### ¿Por qué respeta LSP?

1. **Contrato consistente**: Todas las subclases implementan los mismos métodos
2. **Mismas firmas**: Los parámetros y tipos de retorno son consistentes
3. **Mismo comportamiento esperado**: Todos retornan datos en el mismo formato (Dict)
4. **Sustituibilidad**: Cualquier código que use `BaseService` puede usar cualquier servicio derivado sin modificaciones

### Ejemplo de Sustituibilidad:

```python
def procesar_entidades(service: BaseService):
    """Esta función puede recibir CUALQUIER servicio"""
    entidades = service.get_all()  # Funciona con cualquier servicio
    return entidades

# Todos estos son válidos:
procesar_entidades(ElectorService())
procesar_entidades(VotoService())
procesar_entidades(PartidoPoliticoService())
```

### Beneficios del LSP en este proyecto:

1. **Polimorfismo seguro**: Podemos usar servicios intercambiablemente
2. **Testing facilitado**: Es fácil crear mocks siguiendo el contrato
3. **Mantenibilidad**: Nuevos servicios siguen el mismo patrón
4. **Sin condicionales por tipo**: No hay `if isinstance()` en el código

## 4. Interface Segregation Principle (ISP)

**Las interfaces son específicas y no obligan a implementar métodos innecesarios**

### Ejemplos:

- **BaseService** define solo 3 métodos esenciales: `get_all`, `get_by_id`, `create`
- No fuerza a implementar métodos que algunas entidades no necesiten
- Las clases solo implementan lo que realmente usan

## 5. Dependency Inversion Principle (DIP)

**Los módulos de alto nivel no dependen de módulos de bajo nivel, ambos dependen de abstracciones**

### Ejemplos:

- **Controllers dependen de Services (abstracción)**, no de modelos directamente
  ```python
  # En elector_controller.py
  elector_service = ElectorService()  # Usa el servicio, no el modelo
  electores = elector_service.get_all()
  ```

- **Services dependen de Models**, pero a través de SQLAlchemy (abstracción)
  ```python
  # En base_service.py
  def __init__(self, model):
      self.model = model  # Recibe el modelo como dependencia
  ```

## Beneficios de Aplicar SOLID

1. **Mantenibilidad**: Código más fácil de mantener y entender
2. **Escalabilidad**: Fácil agregar nuevas funcionalidades
3. **Testabilidad**: Componentes independientes son más fáciles de probar
4. **Reutilización**: Clases base pueden reutilizarse
5. **Flexibilidad**: Cambios en una parte no afectan otras

## Diagrama de Arquitectura

```
┌─────────────────┐
│   Controllers   │  (Endpoints HTTP)
│   - GET/POST    │
└────────┬────────┘
         │ Usa
         ▼
┌─────────────────┐
│    Services     │  (Lógica de Negocio)
│  - BaseService  │  ◄─── Aplicación explícita de LSP
│  - Derivados    │
└────────┬────────┘
         │ Usa
         ▼
┌─────────────────┐
│     Models      │  (Estructura de Datos)
│  - SQLAlchemy   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │  (Base de Datos)
└─────────────────┘
```

## Extensión del Sistema

Para agregar una nueva entidad al sistema:

1. **Crear modelo** en `app/models/nueva_entidad.py`
2. **Crear servicio** heredando de `BaseService` (automáticamente cumple LSP)
3. **Crear controller** con endpoints GET y POST
4. **Registrar blueprint** en `app/__init__.py`

Este flujo garantiza que se mantengan los principios SOLID en todo momento.
