from flask import Blueprint, request, jsonify
from app.services import VotoService
from app.models import Elector, TipoVoto
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

@voto_bp.route('/', methods=['POST'])
def create_voto():
    """
    Crea un nuevo voto con sus votos por categoría
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
            - id_tipo_voto
          properties:
            dni:
              type: string
              description: DNI del elector (debe existir en la tabla Elector)
              example: "12345678"
            id_tipo_voto:
              type: integer
              description: ID del tipo de voto (1=Válido, 2=Nulo, 3=En Blanco)
              example: 1
            votos_categoria:
              type: array
              description: Votos por categoría (opcional)
              items:
                type: object
                properties:
                  id_categoria:
                    type: integer
                    example: 1
                  id_partido:
                    type: integer
                    example: 1
                  numero_preferencial_1:
                    type: integer
                    example: 101
                  numero_preferencial_2:
                    type: integer
                    example: 102
    responses:
      201:
        description: Voto creado exitosamente
      400:
        description: Error en los datos o DNI no existe
      404:
        description: Recursos no encontrados
    """
    try:
        data = request.get_json()

        # Validar que existan los datos requeridos
        if not data.get('dni'):
            return jsonify({'error': 'El campo dni es requerido'}), 400
        if not data.get('id_tipo_voto'):
            return jsonify({'error': 'El campo id_tipo_voto es requerido'}), 400

        # Validar que el elector exista
        elector = Elector.query.get(data['dni'])
        if not elector:
            return jsonify({
                'error': f'El elector con DNI {data["dni"]} no existe',
                'sugerencia': 'Debe crear el elector primero en /api/electores/'
            }), 404

        # Validar que el tipo de voto exista
        tipo_voto = TipoVoto.query.get(data['id_tipo_voto'])
        if not tipo_voto:
            return jsonify({
                'error': f'El tipo de voto con ID {data["id_tipo_voto"]} no existe',
                'tipos_disponibles': [{'id': tv.id_tipo_voto, 'nombre': tv.nombre_tipo}
                                      for tv in TipoVoto.query.all()]
            }), 404

        voto = voto_service.create(data)
        return jsonify(voto), 201

    except IntegrityError as e:
        return jsonify({
            'error': 'Error de integridad en la base de datos',
            'detalle': 'Verifique que todas las claves foráneas sean válidas'
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
