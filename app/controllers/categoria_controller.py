from flask import Blueprint, request, jsonify
from app.services import CategoriaService

categoria_bp = Blueprint('categoria', __name__, url_prefix='/api/categorias')
categoria_service = CategoriaService()

@categoria_bp.route('/', methods=['GET'])
def get_all_categorias():
    """
    Obtiene todas las categorías
    ---
    tags:
      - Categorías
    responses:
      200:
        description: Lista de categorías
    """
    categorias = categoria_service.get_all()
    return jsonify(categorias), 200

@categoria_bp.route('/<int:id_categoria>', methods=['GET'])
def get_categoria_by_id(id_categoria):
    """
    Obtiene una categoría por ID
    ---
    tags:
      - Categorías
    parameters:
      - name: id_categoria
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Categoría encontrada
      404:
        description: Categoría no encontrada
    """
    categoria = categoria_service.get_by_id(id_categoria)
    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404
    return jsonify(categoria), 200

@categoria_bp.route('/', methods=['POST'])
def create_categoria():
    """
    Crea una nueva categoría
    ---
    tags:
      - Categorías
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre_categoria:
              type: string
            ambito:
              type: string
    responses:
      201:
        description: Categoría creada
      400:
        description: Error en los datos
    """
    try:
        data = request.get_json()
        categoria = categoria_service.create(data)
        return jsonify(categoria), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
