from flask import Blueprint, request, jsonify
from app.services.pregunta_service import pregunta_service

pregunta_bp = Blueprint('pregunta', __name__, url_prefix='/api/preguntas')


@pregunta_bp.route('/', methods=['GET'])
def get_all_preguntas():
    """
    Obtiene todas las preguntas con sus opciones
    ---
    tags:
      - Cuestionario
    summary: Lista de preguntas para el cuestionario
    description: |
      Retorna todas las preguntas disponibles con sus opciones de respuesta.
      IMPORTANTE: No se expone el campo 'es_correcta' por razones éticas.
      El cuestionario es solo para fines estadísticos.
    responses:
      200:
        description: Lista de preguntas con opciones
        schema:
          type: array
          items:
            type: object
            properties:
              id_pregunta:
                type: integer
                description: ID único de la pregunta
              texto:
                type: string
                description: Texto de la pregunta
              opciones:
                type: array
                items:
                  type: object
                  properties:
                    id_opcion:
                      type: integer
                      description: ID único de la opción
                    id_pregunta:
                      type: integer
                      description: ID de la pregunta asociada
                    texto:
                      type: string
                      description: Texto de la opción
        examples:
          application/json:
            - id_pregunta: 1
              texto: "¿Cuál es el período de mandato presidencial en Perú?"
              opciones:
                - id_opcion: 1
                  id_pregunta: 1
                  texto: "4 años"
                - id_opcion: 2
                  id_pregunta: 1
                  texto: "5 años"
    """
    preguntas = pregunta_service.get_all_con_opciones()
    return jsonify(preguntas), 200


@pregunta_bp.route('/<int:pregunta_id>', methods=['GET'])
def get_pregunta_by_id(pregunta_id):
    """
    Obtiene una pregunta específica con sus opciones
    ---
    tags:
      - Cuestionario
    summary: Detalle de una pregunta
    parameters:
      - name: pregunta_id
        in: path
        type: integer
        required: true
        description: ID de la pregunta
    responses:
      200:
        description: Pregunta encontrada
        schema:
          type: object
          properties:
            id_pregunta:
              type: integer
            texto:
              type: string
            opciones:
              type: array
              items:
                type: object
                properties:
                  id_opcion:
                    type: integer
                  texto:
                    type: string
      404:
        description: Pregunta no encontrada
    """
    pregunta = pregunta_service.get_by_id_con_opciones(pregunta_id)
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404
    return jsonify(pregunta), 200


@pregunta_bp.route('/', methods=['POST'])
def create_pregunta():
    """
    Crea una nueva pregunta (uso administrativo)
    ---
    tags:
      - Cuestionario
    summary: Crear pregunta
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - texto
          properties:
            texto:
              type: string
              description: Texto de la pregunta
              example: "¿Cuántos congresistas tiene el Perú?"
    responses:
      201:
        description: Pregunta creada exitosamente
        schema:
          type: object
          properties:
            id_pregunta:
              type: integer
            texto:
              type: string
      400:
        description: Error en los datos
    """
    try:
        data = request.get_json()
        if not data or 'texto' not in data:
            return jsonify({'error': 'El campo texto es requerido'}), 400

        pregunta = pregunta_service.create(data)
        return jsonify(pregunta), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
