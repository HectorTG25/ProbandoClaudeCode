from flask import Blueprint, request, jsonify
from app.services.cuestionario_service import cuestionario_service

cuestionario_bp = Blueprint('cuestionario', __name__, url_prefix='/api/cuestionarios')


@cuestionario_bp.route('/', methods=['GET'])
def get_all_cuestionarios():
    """
    Obtiene todos los cuestionarios (solo metadatos)
    ---
    tags:
      - Cuestionario
    summary: Lista de cuestionarios completados
    description: |
      Retorna los cuestionarios registrados.
      Solo incluye ID y fecha, sin datos personales ni respuestas.
      Utilidad: estadísticas de participación.
    responses:
      200:
        description: Lista de cuestionarios
        schema:
          type: array
          items:
            type: object
            properties:
              id_cuestionario:
                type: integer
                description: ID del cuestionario
              fecha:
                type: string
                format: date-time
                description: Fecha de registro
    """
    cuestionarios = cuestionario_service.get_all()
    return jsonify(cuestionarios), 200


@cuestionario_bp.route('/estadisticas', methods=['GET'])
def get_estadisticas():
    """
    Obtiene estadísticas del cuestionario
    ---
    tags:
      - Cuestionario
    summary: Estadísticas de participación
    description: |
      Retorna estadísticas básicas sobre la participación en el cuestionario.
      Solo datos agregados, nunca individuales.
    responses:
      200:
        description: Estadísticas
        schema:
          type: object
          properties:
            total_cuestionarios:
              type: integer
              description: Total de cuestionarios completados
    """
    total = cuestionario_service.contar_cuestionarios()
    return jsonify({'total_cuestionarios': total}), 200


@cuestionario_bp.route('/<int:cuestionario_id>', methods=['GET'])
def get_cuestionario_by_id(cuestionario_id):
    """
    Obtiene un cuestionario por ID
    ---
    tags:
      - Cuestionario
    summary: Detalle de un cuestionario
    parameters:
      - name: cuestionario_id
        in: path
        type: integer
        required: true
        description: ID del cuestionario
    responses:
      200:
        description: Cuestionario encontrado
        schema:
          type: object
          properties:
            id_cuestionario:
              type: integer
            fecha:
              type: string
              format: date-time
            respuestas:
              type: array
              items:
                type: object
                properties:
                  id_cuestionario:
                    type: integer
                  id_pregunta:
                    type: integer
                  id_opcion:
                    type: integer
      404:
        description: Cuestionario no encontrado
    """
    cuestionario = cuestionario_service.get_by_id_con_respuestas(cuestionario_id)
    if not cuestionario:
        return jsonify({'error': 'Cuestionario no encontrado'}), 404
    return jsonify(cuestionario), 200


@cuestionario_bp.route('/', methods=['POST'])
def create_cuestionario():
    """
    Registra un cuestionario con sus respuestas
    ---
    tags:
      - Cuestionario
    summary: Registrar cuestionario completado
    description: |
      Registra un nuevo cuestionario con todas sus respuestas.

      RESTRICCIONES ÉTICAS:
      - No se almacena DNI, IP ni datos identificables
      - Completamente independiente del voto emitido
      - No se proporciona feedback sobre respuestas correctas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - respuestas
          properties:
            respuestas:
              type: array
              description: Lista de respuestas a las preguntas
              items:
                type: object
                required:
                  - id_pregunta
                  - id_opcion
                properties:
                  id_pregunta:
                    type: integer
                    description: ID de la pregunta
                  id_opcion:
                    type: integer
                    description: ID de la opción seleccionada
          example:
            respuestas:
              - id_pregunta: 1
                id_opcion: 2
              - id_pregunta: 2
                id_opcion: 5
              - id_pregunta: 3
                id_opcion: 9
    responses:
      201:
        description: Cuestionario registrado exitosamente
        schema:
          type: object
          properties:
            id_cuestionario:
              type: integer
              description: ID del cuestionario creado
            fecha:
              type: string
              format: date-time
            total_respuestas:
              type: integer
              description: Cantidad de respuestas registradas
            mensaje:
              type: string
              description: Mensaje de confirmación
        examples:
          application/json:
            id_cuestionario: 1
            fecha: "2026-01-14T10:30:00"
            total_respuestas: 5
            mensaje: "Cuestionario registrado exitosamente"
      400:
        description: Error en los datos
        schema:
          type: object
          properties:
            error:
              type: string
              description: Descripción del error
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos requeridos'}), 400

        resultado = cuestionario_service.create(data)
        return jsonify(resultado), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500
