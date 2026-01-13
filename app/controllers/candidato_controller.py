from flask import Blueprint, request, jsonify
from app.services import CandidatoService
from app.models import PartidoPolitico, Categoria
from sqlalchemy.exc import IntegrityError

candidato_bp = Blueprint('candidato', __name__, url_prefix='/api/candidatos')
candidato_service = CandidatoService()

@candidato_bp.route('/', methods=['GET'])
def get_all_candidatos():
    """
    Obtiene todos los candidatos
    ---
    tags:
      - Candidatos
    responses:
      200:
        description: Lista de candidatos
    """
    candidatos = candidato_service.get_all()
    return jsonify(candidatos), 200

@candidato_bp.route('/<int:id_candidato>', methods=['GET'])
def get_candidato_by_id(id_candidato):
    """
    Obtiene un candidato por ID
    ---
    tags:
      - Candidatos
    parameters:
      - name: id_candidato
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Candidato encontrado
      404:
        description: Candidato no encontrado
    """
    candidato = candidato_service.get_by_id(id_candidato)
    if not candidato:
        return jsonify({'error': 'Candidato no encontrado'}), 404
    return jsonify(candidato), 200

@candidato_bp.route('/', methods=['POST'])
def create_candidato():
    """
    Crea un nuevo candidato
    ---
    tags:
      - Candidatos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nombre_candidato
            - id_partido
            - id_categoria
          properties:
            nombre_candidato:
              type: string
              description: Nombre completo del candidato
              example: "Juan Pérez García"
            numero_candidato:
              type: integer
              description: Número del candidato (null para Presidente y Vicepresidente)
              example: 101
            id_partido:
              type: integer
              description: ID del partido político
              example: 1
            id_categoria:
              type: integer
              description: ID de la categoría (1=Presidente, 2=Vicepresidente, etc.)
              example: 3
    responses:
      201:
        description: Candidato creado exitosamente
      400:
        description: Error en los datos
      404:
        description: Partido o categoría no encontrados
    """
    try:
        data = request.get_json()

        # Validar campos requeridos
        if not data.get('nombre_candidato'):
            return jsonify({'error': 'El campo nombre_candidato es requerido'}), 400
        if not data.get('id_partido'):
            return jsonify({'error': 'El campo id_partido es requerido'}), 400
        if not data.get('id_categoria'):
            return jsonify({'error': 'El campo id_categoria es requerido'}), 400

        # Validar que el partido exista
        partido = PartidoPolitico.query.get(data['id_partido'])
        if not partido:
            return jsonify({
                'error': f'El partido con ID {data["id_partido"]} no existe',
                'partidos_disponibles': [{'id': p.id_partido, 'nombre': p.nombre_partido}
                                        for p in PartidoPolitico.query.all()]
            }), 404

        # Validar que la categoría exista
        categoria = Categoria.query.get(data['id_categoria'])
        if not categoria:
            return jsonify({
                'error': f'La categoría con ID {data["id_categoria"]} no existe',
                'categorias_disponibles': [{'id': c.id_categoria, 'nombre': c.nombre_categoria}
                                          for c in Categoria.query.all()]
            }), 404

        # Validar que Presidente y Vicepresidente no tengan numero_candidato
        if categoria.nombre_categoria in ['Presidente', 'Vicepresidente']:
            data['numero_candidato'] = None

        candidato = candidato_service.create(data)
        return jsonify(candidato), 201

    except IntegrityError as e:
        return jsonify({
            'error': 'Error de integridad en la base de datos',
            'detalle': 'Verifique que todas las claves foráneas sean válidas'
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
