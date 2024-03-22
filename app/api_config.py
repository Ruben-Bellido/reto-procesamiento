from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import List
from sqlalchemy.orm import Session, joinedload
from db_config import dbMeasure, dbGenerator, engine

# Inicializar FastAPI
app = FastAPI()

# Clases que componen cada generador
class Measure(BaseModel):
    id: int = 0
    production: float
    state: bool
    datetime: str
    
    @validator('production')
    def production_validator(cls, v):
        # Corregir valor para evitar que sea negativo
        v = abs(v)
        # Si el valor de la producción energética es mayor de 5 se considera erróneo
        if v > 5:
            raise ValueError("La medición introducida es errónea")
        return v

class Location(BaseModel):
    latitude: float
    longitude: float

class Generator(BaseModel):
    id: int
    location: Location
    measure: List[Measure]


# Raíz de la API, muestra una guía de uso
@app.get("/")
async def root():
    return {"welcome": "Bienvenido a FastAPI.",
            "guide": {
                "/generators": "Medidas almacenadas en concentrador, se indica la media de producción del parque eólico (MW).",
                "/generators/{id}": "Datos de cada generador, las medidas son actualizadas cada 10s. El rango de IDs de los generadores es de 1-10."
                }
            }


# Información de los generadores y media de producción del parque eólico
@app.get("/generators")
async def get_generators():
    # Inicia una nueva sesión
    session = Session(engine)
    # Realiza una consulta para obtener todos los generadores y sus medidas asociadas
    generators = session.query(dbGenerator).options(joinedload(dbGenerator.measure)).all()
    # Cerrar la sesión
    session.close()

    # Si no se han encontrado generadores, se indica
    if generators is None:
        return {"warning": f"No se han encontrado generadores"}
    else:
        # Inicializa una lista para almacenar las últimas medidas y un diccionario para la respuesta
        last_production = []
        response = {"mean": 0, "generators": {}}

        # Itera sobre cada generador
        for generator in generators:
            # Inicializa el diccionario que representa la última medida
            last_measure = {}
            # Si no se han encontrado medidas para el generador, se indica
            if not generator.measure:
                last_measure["warning"] = "No se han encontrado medidas"
            else:
                # Ordena las medidas por id y obtiene la última
                lm = sorted(generator.measure, key=lambda m: m.id)[-1]
                # Da formato de objeto Measure a la última medida
                last_measure = Measure(id=lm.id,
                                        production=lm.production,
                                        state=lm.state,
                                        datetime=lm.datetime)
                # Añade la última medida a la lista
                last_production.append(lm.production)
            # Añade el generador y su última medida a la respuesta
            response["generators"][generator.id] = {
                "last_measure": last_measure
            }
        
        # Si el listado de últimas medidas contiene registros
        if last_production:
            # Calcula la media de las últimas medidas
            mean = round(sum(last_production) / len(last_production), 2)
        else:
            mean = 0
        # Añade la media a la respuesta
        response["mean"] = mean

        return response


# Información del generador
@app.get("/generators/{generator_id}")
async def get_generator(generator_id: int):
    # Inicia una nueva sesión
    session = Session(engine)
    # Realiza una consulta para obtener el generador y sus medidas asociadas
    generator = session.query(dbGenerator).options(joinedload(dbGenerator.measure)).get(generator_id)
    # Cerrar la sesión
    session.close()

    # Si no se ha encontrado el generador, se indica
    if generator is None:
        return {"error": f"Generador con ID {generator_id} no encontrado"}
    else:
        # Inicializa el listado de medidas asociadas a su respectivo objeto
        measures = []
        # Itera sobre cada medida
        for m in generator.measure:
            # Añade el objeto Measure
            measures.append(Measure(id=m.id,
                                    production=m.production,
                                    state=m.state,
                                    datetime=m.datetime))
        
        return Generator(
        id=generator.id,
        location=Location(
            latitude=generator.latitude,
            longitude=generator.longitude),
        measure=measures
        )


# Publicar medidas del generador
@app.post("/generators/{generator_id}")
async def post_generator(generator_id: int, Measure: Measure):
    # Crea una nueva sesión
    session = Session(engine)
    # Crea un nuevo objeto Measure
    measure = dbMeasure(generator_id=generator_id,
                        production=Measure.production,
                        state=Measure.state,
                        datetime=Measure.datetime)
    # Añade el nuevo objeto Measure a la sesión
    session.add(measure)
    # Confirma la sesión para insertar los nuevos objetos en la base de datos
    session.commit()
    # Cerrar la sesión
    session.close()

    return {"message": f"Datos almacenados para el generador {generator_id}"}
