from sqlalchemy.orm import Session
from db_config import Base, dbGenerator, dbMeasure, engine

# Crea las tablas en la base de datos
Base.metadata.create_all(engine)

# Crea una nueva sesión
session = Session(engine)
# Crea los 10 generadores
for generator_id in range(1,11):
    # Crea un nuevo objeto Generator
    generator = dbGenerator(id=generator_id,
                            latitude=round(-1.11 * generator_id, 6),
                            longitude=round(1.11 * generator_id, 6))
    # Añade el nuevo objeto Generator a la sesión
    session.add(generator)
# Confirma la sesión para insertar los nuevos objetos en la base de datos
session.commit()
# Cerrar la sesión
session.close()
