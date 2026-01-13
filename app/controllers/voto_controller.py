from flask import Blueprint, request, jsonify
from app.services import VotoService
from app.models import Elector, Voto
from sqlalchemy.exc import IntegrityError

voto_bp = Blueprint('voto', __name__, url_prefix='/api/votos')
voto_service = VotoService()

@voto_bp.route('/', methods=['GET'])
def get_all_votos():
    """
    Obtiene todos los votos
    ---
    tags:
      - Votos
    responses:
      200:
        description: Lista de votos
    """
    votos = voto_service.get_all()
    return jsonify(votos), 200

@voto_bp.route('/<int:id_voto>', methods=['GET'])
def get_voto_by_id(id_voto):
    """
    Obtiene un voto por ID con sus votos por categoría
    ---
    tags:
      - Votos
    parameters:
      - name: id_voto
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Voto encontrado
      404:
        description: Voto no encontrado
    """
    voto = voto_service.get_by_id(id_voto)
    if not voto:
        return jsonify({'error': 'Voto no encontrado'}), 404
    return jsonify(voto), 200

@voto_bp.route('/verificar-dni/<dni>', methods=['GET'])
def verificar_dni(dni):
    """
    Verifica si un DNI ya ha votado
    ---
    tags:
      - Votos
    parameters:
      - name: dni
        in: path
        type: string
        required: true
    responses:
      200:
        description: Estado del DNI
    """
    ya_voto = voto_service.dni_ya_voto(dni)
    return jsonify({
        'dni': dni,
        'ya_voto': ya_voto,
        'puede_votar': not ya_voto
    }), 200

@voto_bp.route('/', methods=['POST'])
def create_voto():
    """
    Crea un nuevo voto con determinación automática del tipo (válido o en blanco)
    ---
    tags:
      - Votos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - dni
          properties:
            dni:
              type: string
              description: DNI del elector (debe existir y no haber votado)
              example: "12345678"
            votos_categoria:
              type: array
              description: Votos por categoría. Si todas tienen id_partido=null, será voto en blanco
              items:
                type: object
                properties:
                  id_categoria:
                    type: integer
                    example: 1
                  id_partido:
                    type: integer
                    description: null para voto en blanco en esta categoría
                    example: 1
                  numero_preferencial_1:
                    type: integer
                    example: 101
                  numero_preferencial_2:
                    type: integer
                    example: 102
    responses:
      201:
        description: Voto creado exitosamente. El tipo se determina automáticamente
      400:
        description: Error en los datos o DNI ya votó
      404:
        description: DNI no existe
      409:
        description: El DNI ya ha votado
    """
    try:
        data = request.get_json()

        # Validar que exista el DNI
        if not data.get('dni'):
            return jsonify({'error': 'El campo dni es requerido'}), 400

        dni = data['dni']

        # Validar que el elector exista
        elector = Elector.query.get(dni)
        if not elector:
            return jsonify({
                'error': f'El elector con DNI {dni} no existe',
                'sugerencia': 'Debe crear el elector primero en /api/electores/'
            }), 404

        # Verificar si el DNI ya votó
        if voto_service.dni_ya_voto(dni):
            # Obtener información del voto existente
            voto_existente = Voto.query.filter_by(dni=dni).first()
            return jsonify({
                'error': f'El elector con DNI {dni} ya ha registrado su voto',
                'mensaje': 'No puede votar más de una vez',
                'voto_existente': {
                    'id_voto': voto_existente.id_voto,
                    'fecha': voto_existente.fecha.isoformat(),
                    'tipo_voto': voto_existente.tipo_voto.nombre_tipo
                },
                'sugerencia': 'Ingrese un DNI diferente que no haya votado'
            }), 409

        # Crear el voto (el tipo se determina automáticamente)
        voto = voto_service.create(data)
        return jsonify({
            'mensaje': 'Voto registrado exitosamente',
            'voto': voto
        }), 201

    except ValueError as e:
        # Error de validación (DNI duplicado, etc.)
        return jsonify({
            'error': str(e),
            'tipo': 'validation_error'
        }), 409

    except IntegrityError as e:
        return jsonify({
            'error': 'Error de integridad en la base de datos',
            'detalle': 'El DNI ya ha votado o hay un problema con las claves foráneas',
            'tipo': 'integrity_error'
        }), 409

    except Exception as e:
        return jsonify({
            'error': str(e),
            'tipo': 'server_error'
        }), 400
