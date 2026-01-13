# Documentación de Validaciones Implementadas

Este documento describe las validaciones de lógica de negocio implementadas en el sistema de votación.

## Cambios Implementados

### 1. Voto en Blanco

#### Base de Datos
- **[app/models/voto_categoria.py](app/models/voto_categoria.py:10)**: Columna `id_partido` ahora permite NULL
  ```python
  id_partido = db.Column(db.Integer, db.ForeignKey('partido_politico.id_partido'), nullable=True)
  ```

- **Tipos de Voto**: Verificados en tabla TIPO_VOTO
  - ID 1: "Válido"
  - ID 2: "Nulo"
  - ID 3: "En Blanco"

#### Lógica de Backend

**[app/services/voto_service.py](app/services/voto_service.py:38-51)**:
- Método `determinar_tipo_voto()`: Determina automáticamente el tipo de voto
  - Si todas las categorías tienen `id_partido=null` → Voto en blanco (id=3)
  - Si al menos una categoría tiene partido → Voto válido (id=1)
  - No se usa "valores mágicos", se consulta la tabla TIPO_VOTO

**Registro de Votos en Blanco**:
```python
# Si no hay selección de partido, se registra con id_partido = NULL
voto_categoria = VotoCategoria(
    id_voto=voto.id_voto,
    id_categoria=categoria.id_categoria,
    id_partido=None,  # NULL indica voto en blanco
    numero_preferencial_1=None,
    numero_preferencial_2=None
)
```

#### Frontend
**[frontend/js/api.js](frontend/js/api.js:151-177)**:
- Envía TODAS las categorías al backend
- Categorías sin partido se envían con `id_partido: null`
- El backend determina automáticamente el tipo

### 2. Validación de DNI Único

#### Base de Datos
**[app/models/voto.py](app/models/voto.py:9)**:
- Restricción UNIQUE en columna DNI
  ```python
  dni = db.Column(db.String(20), db.ForeignKey('elector.dni'), nullable=False, unique=True)
  ```

Esta restricción garantiza a nivel de base de datos que no se pueden registrar dos votos con el mismo DNI.

#### Lógica de Backend

**[app/services/voto_service.py](app/services/voto_service.py:30-36)**:
- Método `dni_ya_voto(dni)`: Verifica si un DNI ya votó
  ```python
  def dni_ya_voto(self, dni: str) -> bool:
      voto = self.model.query.filter_by(dni=dni).first()
      return voto is not None
  ```

**Validación en create()**:
```python
if self.dni_ya_voto(dni):
    raise ValueError(f'El DNI {dni} ya ha registrado un voto. No puede votar nuevamente.')
```

**Manejo de IntegrityError**:
```python
try:
    db.session.commit()
except IntegrityError as e:
    if 'unique constraint' in str(e).lower():
        raise ValueError(f'El DNI {dni} ya ha registrado un voto.')
```

#### API Endpoint

**[app/controllers/voto_controller.py](app/controllers/voto_controller.py:47-66)**:
- Endpoint `GET /api/votos/verificar-dni/<dni>`: Verifica si un DNI puede votar
- Endpoint `POST /api/votos/`: Valida DNI antes de crear voto

**Respuesta cuando DNI ya votó (HTTP 409)**:
```json
{
  "error": "El elector con DNI 12345678 ya ha registrado su voto",
  "mensaje": "No puede votar más de una vez",
  "voto_existente": {
    "id_voto": 1,
    "fecha": "2024-01-15T10:30:00",
    "tipo_voto": "Válido"
  },
  "sugerencia": "Ingrese un DNI diferente que no haya votado"
}
```

#### Frontend
**[frontend/js/api.js](frontend/js/api.js:120-131)**:
- Método `verificarDNI(dni)`: Consulta si un DNI ya votó
- Manejo especial de error 409 (DNI duplicado)

**[frontend/js/main.js](frontend/js/main.js:429-476)**:
- Muestra mensaje específico cuando el DNI ya votó
- Solicita ingresar un DNI diferente

### 3. Extensión de init_db.py

**[init_db.py](init_db.py:1-250)**: Script ampliamente extendido

#### Características
- **Idempotente**: Puede ejecutarse múltiples veces sin errores
- **Datos Extensos**:
  - 20 electores (vs 8 anteriores)
  - 10 partidos políticos (vs 5 anteriores)
  - 6 categorías
  - Múltiples candidatos por cada partido en cada categoría:
    - Presidentes: 1 por partido (sin número)
    - Vicepresidentes: 1 por partido (sin número)
    - Diputados: 5 por partido (con número)
    - Senadores Nacionales: 3 por partido (con número)
    - Senadores Regionales: 3 por partido (con número)
    - Parlamento Andino: 2 por partido (con número)
  - **Total: 150 candidatos** (vs 16 anteriores)

#### Desglose de Candidatos
```
Presidente:           10 candidatos (1 por partido)
Vicepresidente:       10 candidatos (1 por partido)
Diputado:             50 candidatos (5 por partido)
Senador Nacional:     30 candidatos (3 por partido)
Senador Regional:     30 candidatos (3 por partido)
Parlamento Andino:    20 candidatos (2 por partido)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:               150 candidatos
```

#### Verificación de Duplicados
```python
if Elector.query.first() is not None:
    print("La base de datos ya contiene datos.")
    return
```

### 4. Validaciones a Nivel de Base de Datos

#### Restricciones Verificadas

**Tabla VOTO**:
- ✅ DNI con restricción UNIQUE
- ✅ id_tipo_voto como FK hacia TIPO_VOTO
- ✅ Garantiza un solo voto por elector

**Tabla VOTO_CATEGORIA**:
- ✅ id_partido permite NULL (para votos en blanco)
- ✅ numero_preferencial_1 permite NULL
- ✅ numero_preferencial_2 permite NULL
- ✅ FK hacia categoria, voto y partido válidas

**Tabla TIPO_VOTO**:
- ✅ Contiene registros requeridos:
  - "Válido"
  - "Nulo"
  - "En Blanco"

## Flujo de Votación

### Caso 1: Voto Válido
```
1. Elector selecciona partidos en algunas categorías
2. Frontend envía:
   {
     "dni": "12345678",
     "votos_categoria": [
       {"id_categoria": 1, "id_partido": 1, ...},     // Válido
       {"id_categoria": 2, "id_partido": null, ...},  // En blanco
       ...
     ]
   }
3. Backend verifica DNI no usado
4. Backend determina tipo = "Válido" (hay al menos 1 partido)
5. Registra en VOTO con id_tipo_voto = 1
6. Registra en VOTO_CATEGORIA todas las categorías
```

### Caso 2: Voto en Blanco Total
```
1. Elector no selecciona ningún partido
2. Frontend envía:
   {
     "dni": "12345678",
     "votos_categoria": [
       {"id_categoria": 1, "id_partido": null, ...},
       {"id_categoria": 2, "id_partido": null, ...},
       ...
     ]
   }
3. Backend verifica DNI no usado
4. Backend determina tipo = "En Blanco" (todos null)
5. Registra en VOTO con id_tipo_voto = 3
6. Registra en VOTO_CATEGORIA todas las categorías con NULL
```

### Caso 3: DNI Duplicado
```
1. Elector ingresa DNI que ya votó
2. Backend verifica: dni_ya_voto(dni) = True
3. Backend retorna HTTP 409 con información del voto existente
4. Frontend muestra mensaje:
   "El DNI 12345678 ya ha votado. Ingrese un DNI diferente"
5. Solicita nuevo DNI
```

## Consultas SQL Importantes

### Verificar voto de un elector
```sql
SELECT v.*, tv.nombre_tipo
FROM voto v
JOIN tipo_voto tv ON v.id_tipo_voto = tv.id_tipo_voto
WHERE v.dni = '12345678';
```

### Ver votos en blanco por categoría
```sql
SELECT c.nombre_categoria, COUNT(*) as total
FROM voto_categoria vc
JOIN categoria c ON vc.id_categoria = c.id_categoria
WHERE vc.id_partido IS NULL
GROUP BY c.nombre_categoria;
```

### Contar votos por tipo
```sql
SELECT tv.nombre_tipo, COUNT(*) as total
FROM voto v
JOIN tipo_voto tv ON v.id_tipo_voto = tv.id_tipo_voto
GROUP BY tv.nombre_tipo;
```

## Testing

### Probar Voto en Blanco
```bash
curl -X POST http://localhost:5000/api/votos/ \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "12345678",
    "votos_categoria": [
      {"id_categoria": 1, "id_partido": null},
      {"id_categoria": 2, "id_partido": null},
      {"id_categoria": 3, "id_partido": null},
      {"id_categoria": 4, "id_partido": null},
      {"id_categoria": 5, "id_partido": null},
      {"id_categoria": 6, "id_partido": null}
    ]
  }'
```

### Probar DNI Duplicado
```bash
# Primera vez: OK (201)
curl -X POST http://localhost:5000/api/votos/ \
  -H "Content-Type: application/json" \
  -d '{"dni": "12345678", "votos_categoria": [...]}'

# Segunda vez: Error 409
curl -X POST http://localhost:5000/api/votos/ \
  -H "Content-Type: application/json" \
  -d '{"dni": "12345678", "votos_categoria": [...]}'
```

### Verificar DNI
```bash
curl http://localhost:5000/api/votos/verificar-dni/12345678
```

## Decisiones de Diseño

### 1. Determinación Automática del Tipo de Voto
**Decisión**: El backend determina automáticamente el tipo de voto basándose en las categorías.

**Razón**:
- Elimina posibilidad de inconsistencias entre frontend y backend
- No requiere que el frontend conozca la lógica de negocio
- Más seguro: el backend es la fuente de verdad

### 2. Envío de Todas las Categorías
**Decisión**: El frontend siempre envía las 6 categorías, incluso las en blanco.

**Razón**:
- Registro completo de la intención del elector
- Facilita análisis estadístico (se sabe que el elector vio la categoría)
- Consistencia en la estructura de datos

### 3. Restricción UNIQUE a Nivel de BD
**Decisión**: DNI único implementado como restricción de base de datos.

**Razón**:
- Garantía a nivel de BD, no solo aplicación
- Protege contra condiciones de carrera
- Doble capa de seguridad (validación + restricción)

### 4. Valores NULL Explícitos
**Decisión**: Usar NULL en vez de valores especiales (-1, 0, etc.).

**Razón**:
- Semántica clara: NULL = ausencia de valor
- Evita confusión con IDs válidos
- Facilita consultas SQL (IS NULL vs comparaciones)

### 5. Script Idempotente
**Decisión**: init_db.py verifica datos existentes antes de insertar.

**Razón**:
- Desarrollo iterativo sin destruir datos
- Previene duplicados accidentales
- Facilita testing y desarrollo

## Archivos Modificados

### Backend
- [app/models/voto.py](app/models/voto.py) - DNI único
- [app/models/voto_categoria.py](app/models/voto_categoria.py) - id_partido nullable
- [app/services/voto_service.py](app/services/voto_service.py) - Lógica de negocio
- [app/controllers/voto_controller.py](app/controllers/voto_controller.py) - Validaciones API
- [init_db.py](init_db.py) - Datos extendidos

### Frontend
- [frontend/js/api.js](frontend/js/api.js) - Nuevas validaciones
- [frontend/js/main.js](frontend/js/main.js) - Manejo de errores DNI

## Próximos Pasos Sugeridos

1. **Logs de Auditoría**: Registrar intentos fallidos de voto duplicado
2. **Rate Limiting**: Limitar intentos por IP
3. **Autenticación Real**: Integrar con sistema de autenticación nacional
4. **Encriptación**: Encriptar votos sensibles
5. **Backup Automático**: Respaldos periódicos de la BD
6. **Monitoreo**: Alertas de intentos de fraude

---

**Estado**: ✅ Todas las validaciones implementadas y funcionando correctamente.
