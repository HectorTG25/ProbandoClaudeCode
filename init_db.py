from app import create_app
from app.models import db, Elector, TipoVoto, PartidoPolitico, Categoria, Candidato

def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    app = create_app()

    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        print("Tablas creadas exitosamente")

        # Verificar si ya existen datos
        if Elector.query.first() is not None:
            print("La base de datos ya contiene datos. No se insertarán datos de ejemplo.")
            return

        # Insertar datos de ejemplo
        print("Insertando datos de ejemplo...")

        # Tipos de voto (válido, nulo, en blanco)
        tipo_voto_1 = TipoVoto(nombre_tipo='Válido')
        tipo_voto_2 = TipoVoto(nombre_tipo='Nulo')
        tipo_voto_3 = TipoVoto(nombre_tipo='En Blanco')
        db.session.add_all([tipo_voto_1, tipo_voto_2, tipo_voto_3])
        db.session.commit()

        # Electores (varios para poder probar con Swagger)
        electores = [
            Elector(dni='12345678', nombres='Juan Carlos', apellidos='Pérez García', distrito='Lima', region='Lima'),
            Elector(dni='87654321', nombres='María Elena', apellidos='López Torres', distrito='Callao', region='Callao'),
            Elector(dni='11111111', nombres='Pedro José', apellidos='Ramírez Soto', distrito='Miraflores', region='Lima'),
            Elector(dni='22222222', nombres='Ana María', apellidos='Gonzales Ruiz', distrito='San Isidro', region='Lima'),
            Elector(dni='33333333', nombres='Luis Alberto', apellidos='Fernández Cruz', distrito='Cusco', region='Cusco'),
            Elector(dni='44444444', nombres='Carmen Rosa', apellidos='Vargas Díaz', distrito='Arequipa', region='Arequipa'),
            Elector(dni='55555555', nombres='Roberto Carlos', apellidos='Mendoza Silva', distrito='Trujillo', region='La Libertad'),
            Elector(dni='66666666', nombres='Patricia Isabel', apellidos='Castillo Rojas', distrito='Chiclayo', region='Lambayeque'),
        ]
        db.session.add_all(electores)
        db.session.commit()

        # Partidos políticos (con rutas de logos)
        partidos = [
            PartidoPolitico(nombre_partido='Partido Democrático Nacional', logo='static/logos/partido_democratico.png'),
            PartidoPolitico(nombre_partido='Alianza Popular', logo='static/logos/alianza_popular.png'),
            PartidoPolitico(nombre_partido='Movimiento Verde Progresista', logo='static/logos/verde_progresista.png'),
            PartidoPolitico(nombre_partido='Frente Unido', logo='static/logos/frente_unido.png'),
            PartidoPolitico(nombre_partido='Partido Libertad', logo='static/logos/partido_libertad.png'),
        ]
        db.session.add_all(partidos)
        db.session.commit()

        # Categorías (presidente, vicepresidente, diputado, senador, parlamento)
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

        # Candidatos (presidente y vicepresidente sin numero_candidato)
        candidatos = [
            # Presidentes (sin número de candidato)
            Candidato(nombre_candidato='Pedro Sánchez Pérez', numero_candidato=None,
                     id_partido=partidos[0].id_partido, id_categoria=categorias[0].id_categoria),
            Candidato(nombre_candidato='Ana Martínez López', numero_candidato=None,
                     id_partido=partidos[1].id_partido, id_categoria=categorias[0].id_categoria),
            Candidato(nombre_candidato='Carlos Mendoza Ruiz', numero_candidato=None,
                     id_partido=partidos[2].id_partido, id_categoria=categorias[0].id_categoria),

            # Vicepresidentes (sin número de candidato)
            Candidato(nombre_candidato='María García Torres', numero_candidato=None,
                     id_partido=partidos[0].id_partido, id_categoria=categorias[1].id_categoria),
            Candidato(nombre_candidato='Luis Fernández Castro', numero_candidato=None,
                     id_partido=partidos[1].id_partido, id_categoria=categorias[1].id_categoria),
            Candidato(nombre_candidato='Carmen Vargas Díaz', numero_candidato=None,
                     id_partido=partidos[2].id_partido, id_categoria=categorias[1].id_categoria),

            # Diputados (con número de candidato)
            Candidato(nombre_candidato='Roberto Castillo Silva', numero_candidato=101,
                     id_partido=partidos[0].id_partido, id_categoria=categorias[2].id_categoria),
            Candidato(nombre_candidato='Patricia Rojas Mendez', numero_candidato=102,
                     id_partido=partidos[1].id_partido, id_categoria=categorias[2].id_categoria),
            Candidato(nombre_candidato='Jorge Ramírez Cruz', numero_candidato=103,
                     id_partido=partidos[2].id_partido, id_categoria=categorias[2].id_categoria),
            Candidato(nombre_candidato='Sandra López Vega', numero_candidato=104,
                     id_partido=partidos[3].id_partido, id_categoria=categorias[2].id_categoria),

            # Senadores Nacionales (con número de candidato)
            Candidato(nombre_candidato='Alberto Gonzales Ruiz', numero_candidato=201,
                     id_partido=partidos[0].id_partido, id_categoria=categorias[3].id_categoria),
            Candidato(nombre_candidato='Elena Díaz Soto', numero_candidato=202,
                     id_partido=partidos[1].id_partido, id_categoria=categorias[3].id_categoria),

            # Senadores Regionales (con número de candidato)
            Candidato(nombre_candidato='Miguel Torres Pérez', numero_candidato=301,
                     id_partido=partidos[2].id_partido, id_categoria=categorias[4].id_categoria),
            Candidato(nombre_candidato='Rosa Silva Morales', numero_candidato=302,
                     id_partido=partidos[3].id_partido, id_categoria=categorias[4].id_categoria),

            # Parlamento Andino (con número de candidato)
            Candidato(nombre_candidato='Francisco Morales Castro', numero_candidato=401,
                     id_partido=partidos[4].id_partido, id_categoria=categorias[5].id_categoria),
            Candidato(nombre_candidato='Lucía Herrera Vega', numero_candidato=402,
                     id_partido=partidos[0].id_partido, id_categoria=categorias[5].id_categoria),
        ]
        db.session.add_all(candidatos)
        db.session.commit()

        print("\n" + "="*60)
        print("Datos de ejemplo insertados exitosamente")
        print("="*60)
        print(f"✓ {TipoVoto.query.count()} tipos de voto")
        print(f"✓ {Elector.query.count()} electores")
        print(f"✓ {PartidoPolitico.query.count()} partidos políticos")
        print(f"✓ {Categoria.query.count()} categorías")
        print(f"✓ {Candidato.query.count()} candidatos")
        print("="*60)
        print("\nDNIs de electores disponibles para pruebas:")
        for elector in Elector.query.all():
            print(f"  - {elector.dni}: {elector.nombres} {elector.apellidos}")
        print("\nIDs de tipos de voto:")
        for tipo in TipoVoto.query.all():
            print(f"  - ID {tipo.id_tipo_voto}: {tipo.nombre_tipo}")
        print("="*60)

if __name__ == '__main__':
    init_database()
