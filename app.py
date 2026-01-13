from app import create_app
from app.models import db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crear las tablas si no existen
        db.create_all()
        print("Tablas creadas exitosamente")

    # Ejecutar la aplicación
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=True
    )
