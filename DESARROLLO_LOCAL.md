# Sistema de Verificación de DNI

Este documento explica cómo usar SQLite para desarrollo local en lugar de PostgreSQL.

## Desarrollo Local con SQLite

Si no tienes PostgreSQL instalado, puedes usar SQLite para desarrollo:

### Opción 1: Variable de Entorno (Recomendado)

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=sqlite:///voting_db.sqlite
SECRET_KEY=dev-secret-key
FLASK_ENV=development
FLASK_DEBUG=True
```

### Opción 2: Modificar config.py temporalmente

En `config/config.py`, cambia la línea 9:

```python
# De:
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/voting_db')

# A:
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///voting_db.sqlite')
```

**IMPORTANTE:** No commitees este cambio. Es solo para desarrollo local.

## Inicializar Base de Datos

```bash
# Con encoding UTF-8 para Windows
$env:PYTHONIOENCODING="utf-8"; python init_db.py

# O en Linux/Mac
python init_db.py
```

## Ejecutar Servidor

```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

## Probar el Sistema

1. Abre `http://localhost:5000/verificacion.html`
2. Ingresa un DNI de prueba (ver lista en consola después de `init_db.py`)
3. Ejemplo: `12345678`
