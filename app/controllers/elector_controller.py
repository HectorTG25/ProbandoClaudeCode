from flask import Blueprint, request, jsonify
from app.services import ElectorService

elector_bp = Blueprint('elector', __name__, url_prefix='/api/electores')
elector_service = ElectorService()

@elector_bp.route('/', methods=['GET'])
def get_all_electores():
    """
    Obtiene todos los electores
    ---
    tags:
      - Electores
    responses:
      200:
        description: Lista de electores
    """
    electores = elector_service.get_all()
    return jsonify(electores), 200

@elector_bp.route('/<string:dni>', methods=['GET'])
def get_elector_by_dni(dni):
    """
    Obtiene un elector por DNI
    ---
    tags:
      - Electores
    parameters:
      - name: dni
        in: path
        type: string
        required: true
    responses:
      200:
        description: Elector encontrado
      404:
        description: Elector no encontrado
    """
    elector = elector_service.get_by_id(dni)
    if not elector:
        return jsonify({'error': 'Elector no encontrado'}), 404
    return jsonify(elector), 200

@elector_bp.route('/', methods=['POST'])
def create_elector():
    """
    Crea un nuevo elector
    ---
    tags:
      - Electores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            dni:
              type: string
            nombres:
              type: string
            apellidos:
              type: string
            distrito:
              type: string
            region:
              type: string
    responses:
      201:
        description: Elector creado
      400:
        description: Error en los datos
    """
    try:
        data = request.get_json()
        elector = elector_service.create(data)
        return jsonify(elector), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
