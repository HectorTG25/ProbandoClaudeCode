# Documentación del Módulo de Cuestionario de Conocimiento Ciudadano

## Descripción General

El módulo de cuestionario es una funcionalidad **opcional** que se presenta al elector **únicamente después** de haber emitido su voto exitosamente. Su propósito es exclusivamente estadístico: evaluar el nivel de conocimiento general sobre el proceso electoral peruano.

---

## Restricciones Éticas y de Diseño

### Principios Fundamentales

1. **Independencia total del voto**: El cuestionario NO almacena ni relaciona ningún dato con el voto emitido.

2. **Anonimato garantizado**: No se almacena:
   - DNI del elector
   - ID del voto
   - Dirección IP
   - Ningún dato identificable

3. **Carácter opcional**: El elector puede:
   - Aceptar y responder el cuestionario
   - Omitirlo completamente sin consecuencias

4. **Sin retroalimentación**: No se muestra al elector si sus respuestas fueron correctas o incorrectas.

5. **Desacoplamiento**: El módulo de cuestionario es completamente independiente del módulo de votación a nivel de código.

---

## Modelo de Base de Datos

### Diagrama de Entidades

```
┌─────────────────────┐
│    CUESTIONARIO     │
├─────────────────────┤
│ PK id_cuestionario  │
│    fecha            │
└─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────┐      ┌─────────────────────┐
│     RESPUESTA       │      │      PREGUNTA       │
├─────────────────────┤      ├─────────────────────┤
│ PK id_cuestionario  │◄─────│ PK id_pregunta      │
│ PK id_pregunta      │      │    texto            │
│ FK id_opcion        │      └─────────────────────┘
└─────────────────────┘               │
         │                            │ 1:N
         │                            ▼
         │                 ┌─────────────────────┐
         └────────────────►│       OPCION        │
                           ├─────────────────────┤
                           │ PK id_opcion        │
                           │ FK id_pregunta      │
                           │    texto            │
                           │    es_correcta      │
                           └─────────────────────┘
```

### Tabla: CUESTIONARIO

| Campo           | Tipo      | Restricciones       | Descripción                    |
|-----------------|-----------|---------------------|--------------------------------|
| id_cuestionario | INTEGER   | PK, AUTO_INCREMENT  | Identificador único            |
| fecha           | DATETIME  | NOT NULL, DEFAULT   | Fecha de registro              |

### Tabla: PREGUNTA

| Campo       | Tipo         | Restricciones       | Descripción            |
|-------------|--------------|---------------------|------------------------|
| id_pregunta | INTEGER      | PK, AUTO_INCREMENT  | Identificador único    |
| texto       | VARCHAR(500) | NOT NULL            | Texto de la pregunta   |

### Tabla: OPCION

| Campo       | Tipo         | Restricciones       | Descripción                    |
|-------------|--------------|---------------------|--------------------------------|
| id_opcion   | INTEGER      | PK, AUTO_INCREMENT  | Identificador único            |
| id_pregunta | INTEGER      | FK, NOT NULL        | Referencia a pregunta          |
| texto       | VARCHAR(300) | NOT NULL            | Texto de la opción             |
| es_correcta | BOOLEAN      | NOT NULL, DEFAULT F | Indica si es correcta          |

### Tabla: RESPUESTA

| Campo           | Tipo    | Restricciones | Descripción                    |
|-----------------|---------|---------------|--------------------------------|
| id_cuestionario | INTEGER | PK, FK        | Referencia a cuestionario      |
| id_pregunta     | INTEGER | PK, FK        | Referencia a pregunta          |
| id_opcion       | INTEGER | FK, NOT NULL  | Referencia a opción elegida    |

**Nota**: La clave primaria compuesta (id_cuestionario, id_pregunta) garantiza que cada pregunta se responda una sola vez por cuestionario.

---

## Endpoints de la API

### GET /api/preguntas/

Obtiene todas las preguntas con sus opciones.

**Importante**: El campo `es_correcta` NO se expone en la respuesta.

**Respuesta (200):**
```json
[
  {
    "id_pregunta": 1,
    "texto": "¿Cuál es el período de mandato presidencial en Perú?",
    "opciones": [
      {"id_opcion": 1, "id_pregunta": 1, "texto": "3 años"},
      {"id_opcion": 2, "id_pregunta": 1, "texto": "4 años"},
      {"id_opcion": 3, "id_pregunta": 1, "texto": "5 años"},
      {"id_opcion": 4, "id_pregunta": 1, "texto": "6 años"}
    ]
  }
]
```

### GET /api/preguntas/{id}

Obtiene una pregunta específica con sus opciones.

### POST /api/preguntas/

Crea una nueva pregunta (uso administrativo).

**Body:**
```json
{
  "texto": "¿Cuántos congresistas tiene el Perú?"
}
```

### GET /api/cuestionarios/

Obtiene todos los cuestionarios registrados (solo metadatos).

### GET /api/cuestionarios/estadisticas

Obtiene estadísticas de participación.

**Respuesta:**
```json
{
  "total_cuestionarios": 150
}
```

### GET /api/cuestionarios/{id}

Obtiene un cuestionario con sus respuestas.

### POST /api/cuestionarios/

Registra un cuestionario completado con todas sus respuestas.

**Body:**
```json
{
  "respuestas": [
    {"id_pregunta": 1, "id_opcion": 3},
    {"id_pregunta": 2, "id_opcion": 7},
    {"id_pregunta": 3, "id_opcion": 10}
  ]
}
```

**Respuesta (201):**
```json
{
  "id_cuestionario": 1,
  "fecha": "2026-01-14T10:30:00",
  "total_respuestas": 10,
  "mensaje": "Cuestionario registrado exitosamente"
}
```

---

## Flujo del Usuario

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DEL CUESTIONARIO                        │
└─────────────────────────────────────────────────────────────────┘

     ┌──────────────┐
     │ Voto emitido │
     │  exitosamente │
     └──────┬───────┘
            │
            ▼
     ┌──────────────────────────────┐
     │ Modal: "¿Deseas responder    │
     │ el cuestionario?"            │
     │ [No, gracias] [Sí, participar]│
     └──────────────┬───────────────┘
                    │
           ┌────────┴────────┐
           │                 │
     ┌─────▼─────┐     ┌─────▼─────┐
     │ "No, gracias" │     │ "Sí, participar" │
     └─────┬─────┘     └─────┬─────┘
           │                 │
           │           ┌─────▼──────────────┐
           │           │ Cargar preguntas    │
           │           │ desde backend       │
           │           └─────┬──────────────┘
           │                 │
           │           ┌─────▼──────────────┐
           │           │ Mostrar cuestionario│
           │           │ (10 preguntas)      │
           │           └─────┬──────────────┘
           │                 │
           │           ┌─────▼──────────────┐
           │           │ Usuario responde    │
           │           │ todas las preguntas │
           │           └─────┬──────────────┘
           │                 │
           │           ┌─────▼──────────────┐
           │           │ Enviar respuestas   │
           │           │ al backend          │
           │           └─────┬──────────────┘
           │                 │
     ┌─────▼─────────────────▼─────┐
     │ Modal: "Gracias por participar"│
     │ [Finalizar]                  │
     └──────────────────────────────┘
```

---

## Estructura de Archivos

### Backend

```
voting_api/
├── app/
│   ├── models/
│   │   ├── cuestionario.py      # Modelo Cuestionario
│   │   ├── pregunta.py          # Modelo Pregunta
│   │   ├── opcion.py            # Modelo Opcion
│   │   └── respuesta.py         # Modelo Respuesta
│   ├── services/
│   │   ├── pregunta_service.py  # Servicio de preguntas
│   │   └── cuestionario_service.py # Servicio de cuestionarios
│   └── controllers/
│       ├── pregunta_controller.py    # Endpoints de preguntas
│       └── cuestionario_controller.py # Endpoints de cuestionarios
└── init_db.py                   # Datos de ejemplo
```

### Frontend

```
voting_api/frontend/
├── js/
│   └── cuestionario.js          # Lógica del cuestionario
├── css/
│   └── styles.css               # Estilos (sección cuestionario)
└── index.html                   # Modales del cuestionario
```

---

## Preguntas de Ejemplo

El sistema incluye 10 preguntas de conocimiento ciudadano:

1. ¿Cuál es el período de mandato presidencial en Perú?
2. ¿Cuántos congresistas tiene el Congreso de la República del Perú?
3. ¿Qué organismo es responsable de organizar los procesos electorales?
4. ¿A partir de qué edad es obligatorio votar en Perú?
5. ¿Hasta qué edad es obligatorio votar en Perú?
6. ¿Qué tipo de voto se considera cuando el elector marca más de una opción?
7. ¿Qué documento es necesario presentar para votar en Perú?
8. ¿Qué es el voto preferencial?
9. ¿Quién proclama oficialmente al Presidente electo del Perú?
10. ¿En qué año las mujeres peruanas votaron por primera vez?

---

## Regla de Unicidad del Cuestionario

El cuestionario implementa una regla de unicidad basada en el flujo, no en datos personales:

1. **El cuestionario solo se muestra después de un voto exitoso**
2. **Un elector solo puede votar una vez** (validación por DNI en el módulo de votación)
3. **Por lo tanto, un elector solo verá la opción del cuestionario una vez**

Esta implementación garantiza que:
- El cuestionario no necesita almacenar DNI para evitar duplicados
- El anonimato se mantiene completamente
- La unicidad se deriva del sistema de votación existente

---

## Decisiones de Diseño

### ¿Por qué no almacenar DNI en el cuestionario?

Almacenar el DNI rompería el anonimato estadístico y permitiría potencialmente relacionar respuestas con electores específicos. La unicidad se garantiza a través del flujo de la aplicación.

### ¿Por qué no mostrar respuestas correctas?

1. Evita influir en el elector para futuros procesos
2. El propósito es puramente estadístico
3. Mostrar feedback podría generar frustración innecesaria

### ¿Por qué es completamente opcional?

1. El acto de votar no debe condicionarse a actividades adicionales
2. Respetar el tiempo del elector
3. Evitar presión o sesgos en las respuestas

---

## Consultas SQL de Ejemplo

### Obtener estadísticas de respuestas correctas (uso interno)

```sql
-- Total de cuestionarios completados
SELECT COUNT(*) as total_cuestionarios FROM cuestionario;

-- Porcentaje de aciertos por pregunta (análisis interno)
SELECT
    p.texto as pregunta,
    COUNT(r.id_cuestionario) as total_respuestas,
    SUM(CASE WHEN o.es_correcta = TRUE THEN 1 ELSE 0 END) as correctas,
    ROUND(SUM(CASE WHEN o.es_correcta = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as porcentaje_acierto
FROM respuesta r
JOIN pregunta p ON r.id_pregunta = p.id_pregunta
JOIN opcion o ON r.id_opcion = o.id_opcion
GROUP BY p.id_pregunta, p.texto
ORDER BY porcentaje_acierto DESC;
```

---

## Pruebas con Swagger

1. Acceder a `http://localhost:5000/apidocs/`
2. Buscar la sección "Cuestionario"
3. Probar GET /api/preguntas/ para ver las preguntas
4. Probar POST /api/cuestionarios/ con el cuerpo de ejemplo

---

## Integración con el Sistema de Votación

El cuestionario se integra con el flujo de votación de manera no invasiva:

1. **main.js**: Después de un voto exitoso, establece una bandera
2. **Al cerrar el modal de resultado**: Se verifica la bandera
3. **Si es true**: Se llama a `Cuestionario.mostrarInvitacion()`
4. **El usuario decide**: Participar u omitir
5. **Flujo independiente**: El cuestionario maneja su propio ciclo de vida

Esta arquitectura garantiza que el código de votación no se modifica significativamente y el cuestionario permanece desacoplado.
