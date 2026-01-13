from flask import Blueprint, request, jsonify
from app.services import TipoVotoService

tipo_voto_bp = Blueprint('tipo_voto', __name__, url_prefix='/api/tipos-voto')
tipo_voto_service = TipoVotoService()

@tipo_voto_bp.route('/', methods=['GET'])
def get_all_tipos_voto():
    """
    Obtiene todos los tipos de voto
    ---
    tags:
      - Tipos de Voto
    responses:
      200:
        description: Lista de tipos de voto
    """
    tipos = tipo_voto_service.get_all()
    return jsonify(tipos), 200

@tipo_voto_bp.route('/<int:id_tipo_voto>', methods=['GET'])
def get_tipo_voto_by_id(id_tipo_voto):
    """
    Obtiene un tipo de voto por ID
    ---
    tags:
      - Tipos de Voto
    parameters:
      - name: id_tipo_voto
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tipo de voto encontrado
      404:
        description: Tipo de voto no encontrado
    """
    tipo = tipo_voto_service.get_by_id(id_tipo_voto)
    if not tipo:
        return jsonify({'error': 'Tipo de voto no encontrado'}), 404
    return jsonify(tipo), 200

@tipo_voto_bp.route('/', methods=['POST'])
def create_tipo_voto():
    """
    Crea un nuevo tipo de voto
    ---
    tags:
      - Tipos de Voto
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre_tipo:
              type: string
    responses:
      201:
        description: Tipo de voto creado
      400:
        description: Error en los datos
    """
    try:
        data = request.get_json()
        tipo = tipo_voto_service.create(data)
        return jsonify(tipo), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
