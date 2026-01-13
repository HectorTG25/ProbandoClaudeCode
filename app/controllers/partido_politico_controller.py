from flask import Blueprint, request, jsonify
from app.services import PartidoPoliticoService

partido_politico_bp = Blueprint('partido_politico', __name__, url_prefix='/api/partidos')
partido_politico_service = PartidoPoliticoService()

@partido_politico_bp.route('/', methods=['GET'])
def get_all_partidos():
    """
    Obtiene todos los partidos políticos
    ---
    tags:
      - Partidos Políticos
    responses:
      200:
        description: Lista de partidos políticos
    """
    partidos = partido_politico_service.get_all()
    return jsonify(partidos), 200

@partido_politico_bp.route('/<int:id_partido>', methods=['GET'])
def get_partido_by_id(id_partido):
    """
    Obtiene un partido político por ID
    ---
    tags:
      - Partidos Políticos
    parameters:
      - name: id_partido
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Partido político encontrado
      404:
        description: Partido político no encontrado
    """
    partido = partido_politico_service.get_by_id(id_partido)
    if not partido:
        return jsonify({'error': 'Partido político no encontrado'}), 404
    return jsonify(partido), 200

@partido_politico_bp.route('/', methods=['POST'])
def create_partido():
    """
    Crea un nuevo partido político
    ---
    tags:
      - Partidos Políticos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre_partido:
              type: string
            logo:
              type: string
    responses:
      201:
        description: Partido político creado
      400:
        description: Error en los datos
    """
    try:
        data = request.get_json()
        partido = partido_politico_service.create(data)
        return jsonify(partido), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
