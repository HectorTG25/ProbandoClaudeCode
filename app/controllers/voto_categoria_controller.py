from flask import Blueprint, request, jsonify
from app.services import VotoCategoriaService
from app.models import Voto, Categoria, PartidoPolitico
from sqlalchemy.exc import IntegrityError

voto_categoria_bp = Blueprint('voto_categoria', __name__, url_prefix='/api/votos-categoria')
voto_categoria_service = VotoCategoriaService()

@voto_categoria_bp.route('/', methods=['GET'])
def get_all_votos_categoria():
    """
    Obtiene todos los votos por categoría
    ---
    tags:
      - Votos por Categoría
    responses:
      200:
        description: Lista de votos por categoría
    """
    votos_categoria = voto_categoria_service.get_all()
    return jsonify(votos_categoria), 200

@voto_categoria_bp.route('/<int:id_voto_categoria>', methods=['GET'])
def get_voto_categoria_by_id(id_voto_categoria):
    """
    Obtiene un voto por categoría por ID
    ---
    tags:
      - Votos por Categoría
    parameters:
      - name: id_voto_categoria
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Voto por categoría encontrado
      404:
        description: Voto por categoría no encontrado
    """
    voto_categoria = voto_categoria_service.get_by_id(id_voto_categoria)
    if not voto_categoria:
        return jsonify({'error': 'Voto por categoría no encontrado'}), 404
    return jsonify(voto_categoria), 200

@voto_categoria_bp.route('/', methods=['POST'])
def create_voto_categoria():
    """
    Crea un nuevo voto por categoría
    NOTA: Es preferible crear votos con sus categorías usando el endpoint /api/votos/
    ---
    tags:
      - Votos por Categoría
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id_voto
            - id_categoria
            - id_partido
          properties:
            id_voto:
              type: integer
              description: ID del voto (debe existir)
              example: 1
            id_categoria:
              type: integer
              description: ID de la categoría
              example: 1
            id_partido:
              type: integer
              description: ID del partido político
              example: 1
            numero_preferencial_1:
              type: integer
              description: Primer número preferencial (opcional)
              example: 101
            numero_preferencial_2:
              type: integer
              description: Segundo número preferencial (opcional)
              example: 102
    responses:
      201:
        description: Voto por categoría creado exitosamente
      400:
        description: Error en los datos
      404:
        description: Voto, categoría o partido no encontrados
    """
    try:
        data = request.get_json()

        # Validar campos requeridos
        if not data.get('id_voto'):
            return jsonify({'error': 'El campo id_voto es requerido'}), 400
        if not data.get('id_categoria'):
            return jsonify({'error': 'El campo id_categoria es requerido'}), 400
        if not data.get('id_partido'):
            return jsonify({'error': 'El campo id_partido es requerido'}), 400

        # Validar que el voto exista
        voto = Voto.query.get(data['id_voto'])
        if not voto:
            return jsonify({
                'error': f'El voto con ID {data["id_voto"]} no existe',
                'sugerencia': 'Debe crear el voto primero en /api/votos/'
            }), 404

        # Validar que la categoría exista
        categoria = Categoria.query.get(data['id_categoria'])
        if not categoria:
            return jsonify({
                'error': f'La categoría con ID {data["id_categoria"]} no existe',
                'categorias_disponibles': [{'id': c.id_categoria, 'nombre': c.nombre_categoria}
                                          for c in Categoria.query.all()]
            }), 404

        # Validar que el partido exista
        partido = PartidoPolitico.query.get(data['id_partido'])
        if not partido:
            return jsonify({
                'error': f'El partido con ID {data["id_partido"]} no existe',
                'partidos_disponibles': [{'id': p.id_partido, 'nombre': p.nombre_partido}
                                        for p in PartidoPolitico.query.all()]
            }), 404

        voto_categoria = voto_categoria_service.create(data)
        return jsonify(voto_categoria), 201

    except IntegrityError as e:
        return jsonify({
            'error': 'Error de integridad en la base de datos',
            'detalle': 'Verifique que todas las claves foráneas sean válidas'
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
