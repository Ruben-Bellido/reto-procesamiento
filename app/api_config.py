from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

# Inicializar FastAPI
app = FastAPI()

# Clases que componen cada generador
class Data(BaseModel):
    production: float
    state: bool
    datetime: str

class Location(BaseModel):
    latitude: float
    longitude: float

class Generator(BaseModel):
    generator_id: int
    location: Location
    measure: Dict[int, Data]


# Registro de generadores en memoria
generator_data = {}
# Inicializar generadores
for generator_id in range(1,11):
    generator_data[generator_id] = Generator(
    generator_id=generator_id,
    location=Location(
        latitude=round(-1.11 * generator_id, 6),
        longitude=round(1.11 * generator_id, 6)),
    measure_id={}
    )


# Raíz de la API, incluye una guía de uso
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
    mean = 0
    generators = {}
    # Generar respuesta con las últimas 
    for generator_id in range(1,len(generator_data)+1):
        # Si no se han hecho mediciones aún se indica mediante un mensaje
        try:
            last = list(generator_data[generator_id].measure.keys())[-1]
            mean += generator_data[generator_id].measure[last].production
            # Añadir descripción y última medición del generador
            generators[generator_id] = {
                    "desc": f"Descripción del generador eólico {generator_id}",
                    "last_measure": generator_data[generator_id].measure[last]
                    }
        except IndexError:
            generators[generator_id] = {
                    "desc": f"Descripción del generador eólico {generator_id}",
                    "last_measure": "Sin mediciones recientes"
                    }
    
    # Calcular la media de producción del parque
    mean = round(mean / len(generator_data), 2)

    return {"mean": mean, "generators": generators}


# Información de cada generador
@app.get("/generators/{generator_id}")
async def get_generator_data(generator_id: int):
    # Si se encuentra el identificador del generador devuelve la información almacenada, en caso contrario devuelve un mensaje de error
    return generator_data.get(generator_id, {"error": f"Generador con ID {generator_id} no encontrado"})


# Publicar datos de cada generador
@app.post("/generators/{generator_id}")
async def post_generator_data(generator_id: int, data: Generator):
    # Si el valor de la producción energética es negativo se considera erróneo
    last = list(data.measure.keys())[-1]
    if data.measure[last].production < 0:
        return {"error": f"Los datos del generador {generator_id} son erróneos"}
    else:
        
        generator_data[generator_id].measure.update(data.measure)
    return {"message": f"Datos almacenados para el generador {generator_id}"}
