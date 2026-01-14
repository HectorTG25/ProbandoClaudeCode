from app import create_app
from app.models import db, Elector, TipoVoto, PartidoPolitico, Categoria, Candidato, Pregunta, Opcion

def init_database():
    """
    Inicializa la base de datos con datos de ejemplo extensos.
    Script idempotente: puede ejecutarse múltiples veces sin errores.
    """
    app = create_app()

    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        print("Tablas creadas exitosamente")

        # Verificar si ya existen datos
        if Elector.query.first() is not None:
            print("\n" + "="*70)
            print("La base de datos ya contiene datos.")
            print("Si desea reiniciar, elimine la base de datos y vuelva a ejecutar.")
            print("="*70)
            return

        print("\nInsertando datos de ejemplo extensos...")

        # ===== TIPOS DE VOTO =====
        print("  → Insertando tipos de voto...")
        tipos_voto = [
            TipoVoto(nombre_tipo='Válido'),
            TipoVoto(nombre_tipo='Nulo'),
            TipoVoto(nombre_tipo='En Blanco')
        ]
        db.session.add_all(tipos_voto)
        db.session.commit()

        # ===== ELECTORES (20 electores) =====
        print("  → Insertando electores...")
        electores = [
            Elector(dni='12345678', nombres='Juan Carlos', apellidos='Pérez García', distrito='Lima', region='Lima'),
            Elector(dni='87654321', nombres='María Elena', apellidos='López Torres', distrito='Callao', region='Callao'),
            Elector(dni='11111111', nombres='Pedro José', apellidos='Ramírez Soto', distrito='Miraflores', region='Lima'),
            Elector(dni='22222222', nombres='Ana María', apellidos='Gonzales Ruiz', distrito='San Isidro', region='Lima'),
            Elector(dni='33333333', nombres='Luis Alberto', apellidos='Fernández Cruz', distrito='Cusco', region='Cusco'),
            Elector(dni='44444444', nombres='Carmen Rosa', apellidos='Vargas Díaz', distrito='Arequipa', region='Arequipa'),
            Elector(dni='55555555', nombres='Roberto Carlos', apellidos='Mendoza Silva', distrito='Trujillo', region='La Libertad'),
            Elector(dni='66666666', nombres='Patricia Isabel', apellidos='Castillo Rojas', distrito='Chiclayo', region='Lambayeque'),
            Elector(dni='77777777', nombres='Jorge Luis', apellidos='Martínez Pérez', distrito='Piura', region='Piura'),
            Elector(dni='88888888', nombres='Rosa María', apellidos='Sánchez Vega', distrito='Iquitos', region='Loreto'),
            Elector(dni='99999999', nombres='Carlos Alberto', apellidos='Gutiérrez Rojas', distrito='Huancayo', region='Junín'),
            Elector(dni='10101010', nombres='Laura Patricia', apellidos='Ríos Mendoza', distrito='Tacna', region='Tacna'),
            Elector(dni='20202020', nombres='Miguel Ángel', apellidos='Torres Castro', distrito='Puno', region='Puno'),
            Elector(dni='30303030', nombres='Sandra Luz', apellidos='Flores Díaz', distrito='Ayacucho', region='Ayacucho'),
            Elector(dni='40404040', nombres='Fernando José', apellidos='Herrera López', distrito='Cajamarca', region='Cajamarca'),
            Elector(dni='50505050', nombres='Gabriela María', apellidos='Silva Romero', distrito='Huaraz', region='Áncash'),
            Elector(dni='60606060', nombres='Ricardo Antonio', apellidos='Morales Vega', distrito='Ica', region='Ica'),
            Elector(dni='70707070', nombres='Verónica Isabel', apellidos='Castro Ruiz', distrito='Tumbes', region='Tumbes'),
            Elector(dni='80808080', nombres='Daniel Eduardo', apellidos='Paredes Soto', distrito='Moyobamba', region='San Martín'),
            Elector(dni='90909090', nombres='Claudia Fernanda', apellidos='Núñez García', distrito='Huánuco', region='Huánuco'),
        ]
        db.session.add_all(electores)
        db.session.commit()

        # ===== PARTIDOS POLÍTICOS (10 partidos) =====
        print("  → Insertando partidos políticos...")
        partidos = [
            PartidoPolitico(nombre_partido='Partido Democrático Nacional', logo='static/logos/partido_democratico.png'),
            PartidoPolitico(nombre_partido='Alianza Popular', logo='static/logos/alianza_popular.png'),
            PartidoPolitico(nombre_partido='Movimiento Verde Progresista', logo='static/logos/verde_progresista.png'),
            PartidoPolitico(nombre_partido='Frente Unido por el Perú', logo='static/logos/frente_unido.png'),
            PartidoPolitico(nombre_partido='Partido Libertad y Democracia', logo='static/logos/partido_libertad.png'),
            PartidoPolitico(nombre_partido='Acción Nacional', logo='static/logos/accion_nacional.png'),
            PartidoPolitico(nombre_partido='Renovación Popular', logo='static/logos/renovacion_popular.png'),
            PartidoPolitico(nombre_partido='Perú Libre', logo='static/logos/peru_libre.png'),
            PartidoPolitico(nombre_partido='Fuerza Popular', logo='static/logos/fuerza_popular.png'),
            PartidoPolitico(nombre_partido='Juntos por el Perú', logo='static/logos/juntos_peru.png'),
        ]
        db.session.add_all(partidos)
        db.session.commit()

        # ===== CATEGORÍAS =====
        print("  → Insertando categorías...")
        categorias = [
            Categoria(nombre_categoria='Presidente', ambito='Nacional'),
            Categoria(nombre_categoria='Vicepresidente', ambito='Nacional'),
            Categoria(nombre_categoria='Diputado', ambito='Nacional'),
            Categoria(nombre_categoria='Senador Nacional', ambito='Nacional'),
            Categoria(nombre_categoria='Senador Regional', ambito='Regional'),
            Categoria(nombre_categoria='Parlamento Andino', ambito='Nacional'),
        ]
        db.session.add_all(categorias)
        db.session.commit()

        # ===== CANDIDATOS (múltiples candidatos por partido y categoría) =====
        print("  → Insertando candidatos...")

        candidatos = []

        # --- PRESIDENTES (sin número) - 1 por partido ---
        nombres_presidentes = [
            'Carlos Enrique Mendoza López', 'María Teresa Rojas Vega', 'José Luis Fernández Castro',
            'Ana Sofía García Ruiz', 'Pedro Antonio Sánchez Díaz', 'Rosa Elena Torres Pérez',
            'Miguel Ángel Vargas Morales', 'Carmen Lucía Herrera Silva', 'Roberto Carlos Ramírez Cruz',
            'Patricia Isabel Flores Mendoza'
        ]
        for i, partido in enumerate(partidos):
            candidatos.append(Candidato(
                nombre_candidato=nombres_presidentes[i],
                numero_candidato=None,
                id_partido=partido.id_partido,
                id_categoria=categorias[0].id_categoria  # Presidente
            ))

        # --- VICEPRESIDENTES (sin número) - 1 por partido ---
        nombres_vices = [
            'Laura Patricia Castillo Rojas', 'Fernando José Gutiérrez López', 'Sandra Luz Paredes Vega',
            'Ricardo Antonio Morales Castro', 'Gabriela María Silva Romero', 'Daniel Eduardo Herrera Díaz',
            'Verónica Isabel Castro Ruiz', 'Luis Alberto Núñez García', 'Claudia Fernanda Ríos Mendoza',
            'Jorge Enrique Torres Soto'
        ]
        for i, partido in enumerate(partidos):
            candidatos.append(Candidato(
                nombre_candidato=nombres_vices[i],
                numero_candidato=None,
                id_partido=partido.id_partido,
                id_categoria=categorias[1].id_categoria  # Vicepresidente
            ))

        # --- DIPUTADOS (con número) - 5 por partido ---
        nombres_diputados = [
            'Alberto Sánchez', 'Beatriz Torres', 'Carlos Vargas', 'Diana Pérez', 'Eduardo García',
            'Fernanda López', 'Gustavo Rojas', 'Helena Castro', 'Ignacio Vega', 'Julia Morales'
        ]
        numero_base_diputado = 100
        for partido in partidos:
            for j in range(5):  # 5 candidatos por partido
                candidatos.append(Candidato(
                    nombre_candidato=f'{nombres_diputados[j % 10]} {j+1}',
                    numero_candidato=numero_base_diputado + (partido.id_partido - 1) * 10 + j,
                    id_partido=partido.id_partido,
                    id_categoria=categorias[2].id_categoria  # Diputado
                ))

        # --- SENADORES NACIONALES (con número) - 3 por partido ---
        nombres_senadores = [
            'Antonio Ramírez', 'Blanca Silva', 'Cesar Herrera', 'Daniela Flores', 'Emilio Díaz'
        ]
        numero_base_senador_nacional = 200
        for partido in partidos:
            for j in range(3):  # 3 candidatos por partido
                candidatos.append(Candidato(
                    nombre_candidato=f'{nombres_senadores[j % 5]} Nacional {j+1}',
                    numero_candidato=numero_base_senador_nacional + (partido.id_partido - 1) * 10 + j,
                    id_partido=partido.id_partido,
                    id_categoria=categorias[3].id_categoria  # Senador Nacional
                ))

        # --- SENADORES REGIONALES (con número) - 3 por partido ---
        numero_base_senador_regional = 300
        for partido in partidos:
            for j in range(3):  # 3 candidatos por partido
                candidatos.append(Candidato(
                    nombre_candidato=f'{nombres_senadores[j % 5]} Regional {j+1}',
                    numero_candidato=numero_base_senador_regional + (partido.id_partido - 1) * 10 + j,
                    id_partido=partido.id_partido,
                    id_categoria=categorias[4].id_categoria  # Senador Regional
                ))

        # --- PARLAMENTO ANDINO (con número) - 2 por partido ---
        nombres_parlamento = ['Francisco Morales', 'Gloria Castro', 'Héctor Vega', 'Irene López']
        numero_base_parlamento = 400
        for partido in partidos:
            for j in range(2):  # 2 candidatos por partido
                candidatos.append(Candidato(
                    nombre_candidato=f'{nombres_parlamento[j % 4]} Parlamento {j+1}',
                    numero_candidato=numero_base_parlamento + (partido.id_partido - 1) * 10 + j,
                    id_partido=partido.id_partido,
                    id_categoria=categorias[5].id_categoria  # Parlamento Andino
                ))

        # Insertar todos los candidatos
        db.session.add_all(candidatos)
        db.session.commit()

        # ===== PREGUNTAS DEL CUESTIONARIO DE CONOCIMIENTO CIUDADANO =====
        print("  → Insertando preguntas del cuestionario...")

        # Definición de preguntas con sus opciones
        preguntas_data = [
            {
                'texto': '¿Cuál es el período de mandato presidencial en Perú?',
                'opciones': [
                    ('3 años', False),
                    ('4 años', False),
                    ('5 años', True),
                    ('6 años', False)
                ]
            },
            {
                'texto': '¿Cuántos congresistas tiene el Congreso de la República del Perú?',
                'opciones': [
                    ('100 congresistas', False),
                    ('120 congresistas', False),
                    ('130 congresistas', True),
                    ('150 congresistas', False)
                ]
            },
            {
                'texto': '¿Qué organismo es responsable de organizar los procesos electorales en Perú?',
                'opciones': [
                    ('JNE (Jurado Nacional de Elecciones)', False),
                    ('ONPE (Oficina Nacional de Procesos Electorales)', True),
                    ('RENIEC (Registro Nacional de Identificación y Estado Civil)', False),
                    ('El Poder Judicial', False)
                ]
            },
            {
                'texto': '¿A partir de qué edad es obligatorio votar en Perú?',
                'opciones': [
                    ('16 años', False),
                    ('18 años', True),
                    ('21 años', False),
                    ('25 años', False)
                ]
            },
            {
                'texto': '¿Hasta qué edad es obligatorio votar en Perú?',
                'opciones': [
                    ('60 años', False),
                    ('65 años', False),
                    ('70 años', True),
                    ('No hay límite de edad', False)
                ]
            },
            {
                'texto': '¿Qué tipo de voto se considera cuando el elector marca más de una opción en una categoría?',
                'opciones': [
                    ('Voto válido', False),
                    ('Voto en blanco', False),
                    ('Voto nulo', True),
                    ('Voto preferencial', False)
                ]
            },
            {
                'texto': '¿Qué documento es necesario presentar para votar en Perú?',
                'opciones': [
                    ('Pasaporte', False),
                    ('DNI (Documento Nacional de Identidad)', True),
                    ('Carnet de extranjería', False),
                    ('Cualquier documento con foto', False)
                ]
            },
            {
                'texto': '¿Qué es el voto preferencial?',
                'opciones': [
                    ('Votar por el candidato de tu preferencia personal', False),
                    ('Elegir el orden de preferencia de candidatos dentro de una lista', True),
                    ('Votar en blanco cuando no hay candidatos preferidos', False),
                    ('Un voto que vale más que otros', False)
                ]
            },
            {
                'texto': '¿Quién proclama oficialmente al Presidente electo del Perú?',
                'opciones': [
                    ('ONPE', False),
                    ('El Congreso de la República', False),
                    ('JNE (Jurado Nacional de Elecciones)', True),
                    ('El Presidente saliente', False)
                ]
            },
            {
                'texto': '¿En qué año las mujeres peruanas votaron por primera vez en elecciones generales?',
                'opciones': [
                    ('1933', False),
                    ('1956', True),
                    ('1979', False),
                    ('1980', False)
                ]
            }
        ]

        # Insertar preguntas y opciones
        for pregunta_data in preguntas_data:
            pregunta = Pregunta(texto=pregunta_data['texto'])
            db.session.add(pregunta)
            db.session.flush()  # Obtener ID de la pregunta

            for texto_opcion, es_correcta in pregunta_data['opciones']:
                opcion = Opcion(
                    id_pregunta=pregunta.id_pregunta,
                    texto=texto_opcion,
                    es_correcta=es_correcta
                )
                db.session.add(opcion)

        db.session.commit()

        # ===== RESUMEN =====
        print("\n" + "="*70)
        print("✓ DATOS DE EJEMPLO INSERTADOS EXITOSAMENTE")
        print("="*70)
        print("\n--- SISTEMA DE VOTACIÓN ---")
        print(f"  Tipos de Voto:         {TipoVoto.query.count()}")
        print(f"  Electores:             {Elector.query.count()}")
        print(f"  Partidos Políticos:    {PartidoPolitico.query.count()}")
        print(f"  Categorías:            {Categoria.query.count()}")
        print(f"  Candidatos:            {Candidato.query.count()}")
        print("\n--- CUESTIONARIO DE CONOCIMIENTO CIUDADANO ---")
        print(f"  Preguntas:             {Pregunta.query.count()}")
        print(f"  Opciones:              {Opcion.query.count()}")
        print("="*70)

        # Desglose de candidatos por categoría
        print("\nCandidatos por categoría:")
        for cat in categorias:
            count = Candidato.query.filter_by(id_categoria=cat.id_categoria).count()
            print(f"  - {cat.nombre_categoria}: {count} candidatos")

        print("\n" + "="*70)
        print("DNIs DISPONIBLES PARA VOTACIÓN (20 electores):")
        print("="*70)
        for i, elector in enumerate(Elector.query.all(), 1):
            print(f"  {i:2d}. {elector.dni} - {elector.nombres} {elector.apellidos} ({elector.region})")

        print("\n" + "="*70)
        print("TIPOS DE VOTO:")
        print("="*70)
        for tipo in TipoVoto.query.all():
            print(f"  ID {tipo.id_tipo_voto}: {tipo.nombre_tipo}")

        print("\n" + "="*70)
        print("IMPORTANTE:")
        print("  - DNI único por voto (no se puede votar dos veces)")
        print("  - Votos en blanco: todas las categorías sin partido")
        print("  - Tipo de voto se determina automáticamente")
        print("="*70 + "\n")

if __name__ == '__main__':
    init_database()
