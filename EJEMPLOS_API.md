# Ejemplos de Uso de la API de Votación

Este documento contiene ejemplos prácticos para probar la API usando Swagger o curl.

## Prerrequisitos

Asegúrate de haber ejecutado el script de inicialización de datos:

```bash
python init_db.py
```

Este script crea:
- 3 tipos de voto (Válido, Nulo, En Blanco)
- 8 electores con DNIs del 12345678 al 66666666
- 5 partidos políticos
- 6 categorías (Presidente, Vicepresidente, Diputado, Senador Nacional, Senador Regional, Parlamento Andino)
- 16 candidatos

## Acceder a Swagger

Inicia la aplicación:

```bash
python app.py
```

Abre tu navegador en: `http://localhost:5000/api/docs`

---

## Ejemplos de Peticiones POST

### 1. Crear un Nuevo Elector

**Endpoint:** `POST /api/electores/`

**Body:**
```json
{
  "dni": "99999999",
  "nombres": "Carlos Alberto",
  "apellidos": "Mendoza Ríos",
  "distrito": "Miraflores",
  "region": "Lima"
}
```

**Respuesta esperada:**
```json
{
  "dni": "99999999",
  "nombres": "Carlos Alberto",
  "apellidos": "Mendoza Ríos",
  "distrito": "Miraflores",
  "region": "Lima"
}
```

---

### 2. Crear un Voto Simple

**Endpoint:** `POST /api/votos/`

**Body (usando un DNI que ya existe):**
```json
{
  "dni": "12345678",
  "id_tipo_voto": 1
}
```

**Nota:**
- `dni` debe ser de un elector existente (ver lista en consola después de init_db.py)
- `id_tipo_voto`: 1=Válido, 2=Nulo, 3=En Blanco

**Respuesta esperada:**
```json
{
  "id_voto": 1,
  "fecha": "2024-01-15T10:30:00",
  "dni": "12345678",
  "id_tipo_voto": 1,
  "votos_categoria": []
}
```

---

### 3. Crear un Voto Completo con Votos por Categoría

**Endpoint:** `POST /api/votos/`

**Body:**
```json
{
  "dni": "87654321",
  "id_tipo_voto": 1,
  "votos_categoria": [
    {
      "id_categoria": 1,
      "id_partido": 1,
      "numero_preferencial_1": null,
      "numero_preferencial_2": null
    },
    {
      "id_categoria": 3,
      "id_partido": 2,
      "numero_preferencial_1": 101,
      "numero_preferencial_2": 102
    }
  ]
}
```

**Explicación:**
- Primer voto: Categoría Presidente (id=1), Partido Democrático Nacional (id=1), sin preferenciales
- Segundo voto: Categoría Diputado (id=3), Alianza Popular (id=2), con votos preferenciales 101 y 102

**Respuesta esperada:**
```json
{
  "id_voto": 2,
  "fecha": "2024-01-15T10:35:00",
  "dni": "87654321",
  "id_tipo_voto": 1,
  "votos_categoria": [
    {
      "id_voto_categoria": 1,
      "id_voto": 2,
      "id_categoria": 1,
      "id_partido": 1,
      "numero_preferencial_1": null,
      "numero_preferencial_2": null
    },
    {
      "id_voto_categoria": 2,
      "id_voto": 2,
      "id_categoria": 3,
      "id_partido": 2,
      "numero_preferencial_1": 101,
      "numero_preferencial_2": 102
    }
  ]
}
```

---

### 4. Crear un Candidato (Diputado con número)

**Endpoint:** `POST /api/candidatos/`

**Body:**
```json
{
  "nombre_candidato": "Jorge Luis Pérez",
  "numero_candidato": 105,
  "id_partido": 1,
  "id_categoria": 3
}
```

**Nota:** Categoría 3 = Diputado (requiere numero_candidato)

**Respuesta esperada:**
```json
{
  "id_candidato": 17,
  "nombre_candidato": "Jorge Luis Pérez",
  "numero_candidato": 105,
  "id_partido": 1,
  "id_categoria": 3
}
```

---

### 5. Crear un Candidato (Presidente sin número)

**Endpoint:** `POST /api/candidatos/`

**Body:**
```json
{
  "nombre_candidato": "María Elena Rodríguez",
  "numero_candidato": null,
  "id_partido": 4,
  "id_categoria": 1
}
```

**Nota:** Categoría 1 = Presidente (no requiere numero_candidato, se establece automáticamente como null)

**Respuesta esperada:**
```json
{
  "id_candidato": 18,
  "nombre_candidato": "María Elena Rodríguez",
  "numero_candidato": null,
  "id_partido": 4,
  "id_categoria": 1
}
```

---

### 6. Crear un Partido Político

**Endpoint:** `POST /api/partidos/`

**Body:**
```json
{
  "nombre_partido": "Nuevo Partido Democrático",
  "logo": "static/logos/nuevo_partido.png"
}
```

**Respuesta esperada:**
```json
{
  "id_partido": 6,
  "nombre_partido": "Nuevo Partido Democrático",
  "logo": "static/logos/nuevo_partido.png"
}
```

---

### 7. Crear una Categoría

**Endpoint:** `POST /api/categorias/`

**Body:**
```json
{
  "nombre_categoria": "Gobernador Regional",
  "ambito": "Regional"
}
```

**Respuesta esperada:**
```json
{
  "id_categoria": 7,
  "nombre_categoria": "Gobernador Regional",
  "ambito": "Regional"
}
```

---

### 8. Crear un Tipo de Voto

**Endpoint:** `POST /api/tipos-voto/`

**Body:**
```json
{
  "nombre_tipo": "Electrónico"
}
```

**Respuesta esperada:**
```json
{
  "id_tipo_voto": 4,
  "nombre_tipo": "Electrónico"
}
```

---

## Errores Comunes y Soluciones

### Error: DNI no existe

**Error:**
```json
{
  "error": "El elector con DNI 99999999 no existe",
  "sugerencia": "Debe crear el elector primero en /api/electores/"
}
```

**Solución:** Crear el elector primero usando `POST /api/electores/`

---

### Error: ID de tipo de voto no válido

**Error:**
```json
{
  "error": "El tipo de voto con ID 99 no existe",
  "tipos_disponibles": [
    {"id": 1, "nombre": "Válido"},
    {"id": 2, "nombre": "Nulo"},
    {"id": 3, "nombre": "En Blanco"}
  ]
}
```

**Solución:** Usar uno de los IDs disponibles listados en la respuesta.

---

### Error: Partido o Categoría no existe

**Error:**
```json
{
  "error": "El partido con ID 99 no existe",
  "partidos_disponibles": [
    {"id": 1, "nombre": "Partido Democrático Nacional"},
    {"id": 2, "nombre": "Alianza Popular"},
    ...
  ]
}
```

**Solución:** Usar uno de los IDs disponibles o crear el partido primero.

---

## Ejemplos con curl

### Crear un elector:
```bash
curl -X POST http://localhost:5000/api/electores/ \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "77777777",
    "nombres": "Test",
    "apellidos": "Usuario",
    "distrito": "Lima",
    "region": "Lima"
  }'
```

### Crear un voto:
```bash
curl -X POST http://localhost:5000/api/votos/ \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "12345678",
    "id_tipo_voto": 1
  }'
```

### Obtener todos los electores:
```bash
curl http://localhost:5000/api/electores/
```

### Obtener un voto específico:
```bash
curl http://localhost:5000/api/votos/1
```

---

## IDs de Referencia (después de ejecutar init_db.py)

### DNIs de Electores Disponibles:
- 12345678: Juan Carlos Pérez García
- 87654321: María Elena López Torres
- 11111111: Pedro José Ramírez Soto
- 22222222: Ana María Gonzales Ruiz
- 33333333: Luis Alberto Fernández Cruz
- 44444444: Carmen Rosa Vargas Díaz
- 55555555: Roberto Carlos Mendoza Silva
- 66666666: Patricia Isabel Castillo Rojas

### IDs de Tipos de Voto:
- 1: Válido
- 2: Nulo
- 3: En Blanco

### IDs de Categorías:
- 1: Presidente
- 2: Vicepresidente
- 3: Diputado
- 4: Senador Nacional
- 5: Senador Regional
- 6: Parlamento Andino

### IDs de Partidos:
- 1: Partido Democrático Nacional
- 2: Alianza Popular
- 3: Movimiento Verde Progresista
- 4: Frente Unido
- 5: Partido Libertad

---

## Notas Importantes

1. **Presidente y Vicepresidente no tienen numero_candidato**: Estos candidatos deben tener `numero_candidato: null`

2. **Votos y Votos por Categoría van juntos**: Es mejor crear un voto con sus categorías en una sola petición usando el endpoint `/api/votos/` con el array `votos_categoria`

3. **Validación de FK automática**: Todos los endpoints POST validan automáticamente que las claves foráneas existan y proporcionan mensajes de error útiles

4. **Logos de partidos**: Las rutas de logos deben apuntar a `static/logos/nombre_archivo.png`

5. **Consultar datos disponibles**: Usa los endpoints GET para ver qué IDs están disponibles antes de crear nuevos registros
