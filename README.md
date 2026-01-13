# API REST de Sistema de Votación

API REST sencilla desarrollada con Flask, PostgreSQL y Swagger para gestionar un sistema de votación electrónica.

## Características

- API REST con endpoints GET y POST
- Base de datos PostgreSQL
- Documentación automática con Swagger/OpenAPI
- Aplicación de principios SOLID (especialmente LSP)
- Separación de responsabilidades (Models, Services, Controllers)
- SQLAlchemy como ORM

## Estructura del Proyecto

```
voting_api/
├── app/
│   ├── __init__.py           # Factory de la aplicación
│   ├── swagger.py            # Configuración de Swagger
│   ├── models/               # Modelos de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── elector.py
│   │   ├── voto.py
│   │   ├── tipo_voto.py
│   │   ├── partido_politico.py
│   │   ├── candidato.py
│   │   ├── categoria.py
│   │   └── voto_categoria.py
│   ├── services/             # Lógica de negocio (aplicación de LSP)
│   │   ├── __init__.py
│   │   ├── base_service.py   # Clase base abstracta
│   │   └── [servicios específicos]
│   └── controllers/          # Endpoints REST
│       ├── __init__.py
│       └── [controllers específicos]
├── config/
│   └── config.py             # Configuración de la aplicación
├── app.py                    # Punto de entrada principal
├── init_db.py                # Script de inicialización de BD
├── requirements.txt          # Dependencias
├── .env.example              # Ejemplo de variables de entorno
└── README.md                 # Este archivo
```

## Modelo de Datos

### Entidades principales:

- **ELECTOR**: dni (PK), nombres, apellidos, distrito, region
- **VOTO**: id_voto (PK), fecha, dni (FK), id_tipo_voto (FK)
- **TIPO_VOTO**: id_tipo_voto (PK), nombre_tipo
- **PARTIDO_POLITICO**: id_partido (PK), nombre_partido, logo
- **CANDIDATO**: id_candidato (PK), nombre_candidato, numero_candidato, id_partido (FK), id_categoria (FK)
- **CATEGORIA**: id_categoria (PK), nombre_categoria, ambito
- **VOTO_CATEGORIA**: id_voto_categoria (PK), id_voto (FK), id_categoria (FK), id_partido (FK), numero_preferencial_1, numero_preferencial_2

## Principios SOLID Aplicados

### 1. Single Responsibility Principle (SRP)
Cada clase tiene una única responsabilidad:
- **Modelos**: Solo representan la estructura de datos
- **Servicios**: Contienen la lógica de negocio
- **Controllers**: Manejan las peticiones HTTP

### 2. Open/Closed Principle (OCP)
El sistema está abierto para extensión pero cerrado para modificación:
- Nuevos servicios pueden heredar de `BaseService` sin modificar código existente
- Nuevos endpoints se agregan como blueprints sin alterar la estructura principal

### 3. Liskov Substitution Principle (LSP)
**Implementación explícita**:
- `BaseService` define un contrato claro con métodos abstractos
- Todos los servicios (ElectorService, VotoService, etc.) implementan este contrato
- Cualquier clase derivada puede sustituir a `BaseService` sin romper la funcionalidad
- No se fuerzan métodos que las clases hijas no puedan implementar correctamente

### 4. Interface Segregation Principle (ISP)
Las interfaces son específicas y no obligan a implementar métodos innecesarios

### 5. Dependency Inversion Principle (DIP)
Los controllers dependen de abstracciones (servicios) no de implementaciones concretas

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd voting_api
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Crear una base de datos en PostgreSQL:

```sql
CREATE DATABASE voting_db;
CREATE USER voting_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE voting_db TO voting_user;
```

### 5. Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```
DATABASE_URL=postgresql://voting_user:your_password@localhost:5432/voting_db
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
```

### 6. Inicializar la base de datos

Ejecutar el script de inicialización que crea las tablas e inserta datos de ejemplo:

```bash
python init_db.py
```

## Ejecución

### Modo desarrollo

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Acceder a la documentación Swagger

Abrir en el navegador: `http://localhost:5000/api/docs`

## Endpoints Disponibles

### Electores
- `GET /api/electores/` - Obtener todos los electores
- `GET /api/electores/<dni>` - Obtener un elector por DNI
- `POST /api/electores/` - Crear un nuevo elector

### Tipos de Voto
- `GET /api/tipos-voto/` - Obtener todos los tipos de voto
- `GET /api/tipos-voto/<id>` - Obtener un tipo de voto por ID
- `POST /api/tipos-voto/` - Crear un nuevo tipo de voto

### Votos
- `GET /api/votos/` - Obtener todos los votos
- `GET /api/votos/<id>` - Obtener un voto por ID
- `POST /api/votos/` - Crear un nuevo voto

### Partidos Políticos
- `GET /api/partidos/` - Obtener todos los partidos
- `GET /api/partidos/<id>` - Obtener un partido por ID
- `POST /api/partidos/` - Crear un nuevo partido

### Candidatos
- `GET /api/candidatos/` - Obtener todos los candidatos
- `GET /api/candidatos/<id>` - Obtener un candidato por ID
- `POST /api/candidatos/` - Crear un nuevo candidato

### Categorías
- `GET /api/categorias/` - Obtener todas las categorías
- `GET /api/categorias/<id>` - Obtener una categoría por ID
- `POST /api/categorias/` - Crear una nueva categoría

### Votos por Categoría
- `GET /api/votos-categoria/` - Obtener todos los votos por categoría
- `GET /api/votos-categoria/<id>` - Obtener un voto por categoría por ID
- `POST /api/votos-categoria/` - Crear un nuevo voto por categoría

## Ejemplos de Uso

### Crear un elector (POST)

```bash
curl -X POST http://localhost:5000/api/electores/ \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "99999999",
    "nombres": "Carlos",
    "apellidos": "Mendoza",
    "distrito": "Miraflores",
    "region": "Lima"
  }'
```

### Obtener todos los electores (GET)

```bash
curl http://localhost:5000/api/electores/
```

### Crear un voto (POST)

```bash
curl -X POST http://localhost:5000/api/votos/ \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "12345678",
    "id_tipo_voto": 1
  }'
```

## Tecnologías Utilizadas

- **Flask 3.0.0**: Framework web
- **Flask-SQLAlchemy 3.1.1**: ORM para Python
- **PostgreSQL**: Base de datos relacional
- **Flasgger 4.11.1**: Integración de Swagger/OpenAPI
- **Flask-CORS 4.0.0**: Manejo de CORS
- **psycopg2-binary 2.9.9**: Adaptador de PostgreSQL
- **python-dotenv 1.0.0**: Gestión de variables de entorno

## Notas de Desarrollo

- El código sigue los principios SOLID, especialmente el LSP mediante la clase `BaseService`
- La separación de responsabilidades permite un mantenimiento sencillo
- Swagger proporciona documentación interactiva automática
- El sistema está diseñado para ser fácilmente extensible

## Demostración de Claude Code

Este proyecto fue creado como demostración de las capacidades de Claude Code, priorizando:
- Buenas prácticas de diseño
- Código limpio y legible
- Aplicación explícita de principios SOLID
- Estructura organizada y escalable
