# Entrypoint para Vercel Serverless Functions
# Este archivo es el punto de entrada que Vercel usa para ejecutar la aplicacion
# NO incluir app.run() - Vercel maneja el servidor internamente

from app import create_app

# Crear la aplicacion Flask con configuracion de produccion
# Vercel busca una variable llamada 'app' o 'application'
app = create_app('production')
