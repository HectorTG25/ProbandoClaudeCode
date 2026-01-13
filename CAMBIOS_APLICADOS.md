# Cambios Aplicados a la API de Votación

Este documento resume todas las correcciones y mejoras implementadas basadas en los requerimientos del usuario.

## Resumen de Correcciones

### 1. Tipos de Voto Actualizados

**Anterior:**
- Presencial
- Virtual

**Nuevo:**
- Válido
- Nulo
- En Blanco

**Archivo modificado:** [init_db.py](init_db.py:23-26)

---

### 2. Partidos Políticos - Rutas de Logos

**Cambio:** Las rutas de logos ahora apuntan a archivos dentro del proyecto.

**Formato:** `static/logos/nombre_partido.png`

**Ejemplos:**
- `static/logos/partido_democratico.png`
- `static/logos/alianza_popular.png`
- `static/logos/verde_progresista.png`

**Carpeta creada:** [static/logos/](static/logos/)

**Archivo modificado:** [init_db.py](init_db.py:48-55)

---

### 3. Categorías Actualizadas

**Anterior:**
- Presidente (Nacional)
- Congresista (Regional)
- Alcalde (Local)

**Nuevo:**
- Presidente (Nacional)
- Vicepresidente (Nacional)
- Diputado (Nacional)
- Senador Nacional (Nacional)
- Senador Regional (Regional)
- Parlamento Andino (Nacional)

**Nota:** Todas las categorías son "Nacional" excepto "Senador Regional" que puede ser tanto Nacional como Regional.

**Archivo modificado:** [init_db.py](init_db.py:58-67)

---

### 4. Modelo Candidato - numero_candidato Opcional

**Cambio:** El campo `numero_candidato` ahora es **nullable** (opcional).

**Regla de negocio:**
- **Presidente y Vicepresidente:** `numero_candidato = NULL`
- **Otras categorías:** `numero_candidato` es requerido (Diputado, Senador, Parlamento)

**Validación automática:** El controller de candidatos establece `numero_candidato = null` automáticamente para Presidente y Vicepresidente.

**Archivos modificados:**
- [app/models/candidato.py](app/models/candidato.py:9) - Modelo actualizado a `nullable=True`
- [app/controllers/candidato_controller.py](app/controllers/candidato_controller.py:118-119) - Validación automática

---

### 5. Relación VOTO ↔ VOTO_CATEGORIA

**Cambio:** Ahora toda inserción en VOTO puede incluir automáticamente sus tuplas en VOTO_CATEGORIA.

**Implementación:**

#### VotoService mejorado
El servicio ahora acepta un array `votos_categoria` en la petición POST:

```json
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
```

**Beneficios:**
- Un solo POST crea el voto y todas sus categorías asociadas
- Transacción atómica (todo o nada)
- Respuesta incluye el voto completo con sus categorías

**Archivos modificados:**
- [app/services/voto_service.py](app/services/voto_service.py:29-73) - Método `create` mejorado
- [app/controllers/voto_controller.py](app/controllers/voto_controller.py:71-88) - Documentación Swagger actualizada

---

### 6. Validación de Claves Foráneas Mejorada

**Problema anterior:** Al hacer POST con un DNI o ID inexistente, la API devolvía un error genérico.

**Solución implementada:** Validación previa con mensajes descriptivos.

#### Ejemplo de error mejorado:

**Antes:**
```json
{
  "error": "foreign key constraint failed"
}
```

**Ahora:**
```json
{
  "error": "El elector con DNI 99999999 no existe",
  "sugerencia": "Debe crear el elector primero en /api/electores/"
}
```

#### Controllers mejorados:

1. **VotoController** ([app/controllers/voto_controller.py](app/controllers/voto_controller.py:97-132))
   - Valida que el DNI del elector exista
   - Valida que el id_tipo_voto exista
   - Proporciona lista de tipos disponibles si falla

2. **CandidatoController** ([app/controllers/candidato_controller.py](app/controllers/candidato_controller.py:88-130))
   - Valida que id_partido exista
   - Valida que id_categoria exista
   - Proporciona listas de partidos/categorías disponibles
   - Establece automáticamente `numero_candidato = null` para Presidente/Vicepresidente

3. **VotoCategoriaController** ([app/controllers/voto_categoria_controller.py](app/controllers/voto_categoria_controller.py:93-139))
   - Valida id_voto, id_categoria, id_partido
   - Proporciona listas de recursos disponibles

---

### 7. Datos de Ejemplo Expandidos

**Electores:** Aumentados de 2 a **8 electores** con DNIs variados para facilitar pruebas.

**DNIs disponibles:**
- 12345678, 87654321, 11111111, 22222222
- 33333333, 44444444, 55555555, 66666666

**Partidos:** Aumentados de 3 a **5 partidos políticos**

**Candidatos:** Aumentados de 4 a **16 candidatos** distribuidos en todas las categorías:
- 3 presidentes
- 3 vicepresidentes
- 4 diputados
- 2 senadores nacionales
- 2 senadores regionales
- 2 parlamentarios andinos

**Archivo modificado:** [init_db.py](init_db.py:30-130)

---

### 8. Salida Mejorada del Script de Inicialización

**Nuevo formato:**

```
============================================================
Datos de ejemplo insertados exitosamente
============================================================
✓ 3 tipos de voto
✓ 8 electores
✓ 5 partidos políticos
✓ 6 categorías
✓ 16 candidatos
============================================================

DNIs de electores disponibles para pruebas:
  - 12345678: Juan Carlos Pérez García
  - 87654321: María Elena López Torres
  ...

IDs de tipos de voto:
  - ID 1: Válido
  - ID 2: Nulo
  - ID 3: En Blanco
============================================================
```

---

## Archivos Nuevos Creados

1. **[EJEMPLOS_API.md](EJEMPLOS_API.md)** - Guía completa con ejemplos de uso
2. **[CAMBIOS_APLICADOS.md](CAMBIOS_APLICADOS.md)** - Este archivo
3. **[static/logos/](static/logos/)** - Carpeta para almacenar logos de partidos

---

## Archivos Modificados

### Modelos
- [app/models/candidato.py](app/models/candidato.py:9) - `numero_candidato` ahora nullable

### Servicios
- [app/services/voto_service.py](app/services/voto_service.py) - Manejo de votos con categorías

### Controllers
- [app/controllers/voto_controller.py](app/controllers/voto_controller.py) - Validaciones FK mejoradas
- [app/controllers/candidato_controller.py](app/controllers/candidato_controller.py) - Validaciones FK mejoradas
- [app/controllers/voto_categoria_controller.py](app/controllers/voto_categoria_controller.py) - Validaciones FK mejoradas

### Configuración
- [init_db.py](init_db.py) - Datos actualizados y expandidos

---

## Mejoras en la Experiencia de Swagger

1. **Documentación más descriptiva** en los endpoints POST
2. **Ejemplos incluidos** en los schemas de Swagger
3. **Mensajes de error útiles** con sugerencias de corrección
4. **Listas de recursos disponibles** cuando hay errores de FK

---

## Cómo Probar los Cambios

### 1. Reiniciar la base de datos

Si ya ejecutaste `init_db.py` antes, elimina la base de datos y vuélvela a crear:

```bash
# Eliminar la base de datos existente (PostgreSQL)
psql -U postgres
DROP DATABASE voting_db;
CREATE DATABASE voting_db;
\q

# Inicializar con los nuevos datos
python init_db.py
```

### 2. Ejecutar la aplicación

```bash
python app.py
```

### 3. Probar en Swagger

Abrir: `http://localhost:5000/api/docs`

### 4. Probar ejemplos

Ver: [EJEMPLOS_API.md](EJEMPLOS_API.md) para casos de uso completos

---

## Validaciones Implementadas

### ✅ Votos
- DNI debe existir en tabla Elector
- id_tipo_voto debe existir en tabla TipoVoto
- votos_categoria (opcional) valida id_categoria, id_partido

### ✅ Candidatos
- id_partido debe existir en tabla PartidoPolitico
- id_categoria debe existir en tabla Categoria
- numero_candidato automáticamente NULL para Presidente/Vicepresidente

### ✅ Votos por Categoría
- id_voto debe existir en tabla Voto
- id_categoria debe existir en tabla Categoria
- id_partido debe existir en tabla PartidoPolitico

---

## Principios SOLID Mantenidos

Todas las mejoras respetan los principios SOLID originales:

- **SRP:** Validaciones en controllers, lógica en services
- **OCP:** Nuevas funcionalidades sin modificar código existente
- **LSP:** Todos los servicios siguen cumpliendo el contrato de BaseService
- **ISP:** Interfaces específicas sin métodos innecesarios
- **DIP:** Dependencia de abstracciones (services), no implementaciones

---

## Notas Finales

- Todas las validaciones son **previas al insert**, evitando errores de base de datos
- Los mensajes de error incluyen **sugerencias** y **listas de recursos disponibles**
- La relación VOTO-VOTO_CATEGORIA es ahora **más intuitiva** mediante un solo POST
- Los datos de ejemplo son **más realistas** y completos para pruebas exhaustivas
