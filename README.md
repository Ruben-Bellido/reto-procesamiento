# reto-procesamiento

## Pasos seguidos
- Comprensión de uso de FastAPI y modelos de Pydantic junto a su verificación de datos
- Planteamiento de los modelos de datos
- Desarrollo de la generación de datos sintéticos
- Configuración de FastAPI
- Envío de datos a FastAPI
- Configuración y generación de una base de datos
- Adaptación de la configuración de FastAPI a la base de datos
- Desarrollo del shell script encargado de instalar todo lo necesario para que el proyecto funcione
 
## Instrucciones de uso
Todos los comandos se han de ejecutar desde la ruta /app
### Módulos y componentes nesesarios:
- $ sh requirements.sh
- $ sudo apt install uvicorn
### Ejecucción del programa:
- Generar la base de datos: $ python3 generate_db.py
- Iniciar la API: $ uvicorn api_config:app --reload
- Generación de datos sintéticos: $ python3
### Uso de la API:
- Guía: Petición GET a http://127.0.0.1:8000
- Media y última medida de todos los generadores: Petición GET a http://127.0.0.1:8000/generators
- Datos de un generador por ID: Petición GET a http://127.0.0.1:8000/generators/{ID}
- Añadir medida a un generador por ID: Petición POST a http://127.0.0.1:8000/generators/{ID} (body raw JSON: {"production": float, "state": bool, "datetime": str})
- Los valores de "production" se han de encontrar en un rango de 0-5 (MW), en caso de ser negativo se corrije automáticamente a positivo, pero si el resultado es mayor que 5 la medida se descarta

## Posibles vías de mejora
- Mejorar la escalabilidad de la aplicación (la generación de datos sintéticos genera medidas para los IDs 1-10 únicamente)
- Aumentar la complejidad de los datos (añadiendo más campos) o de la aplicación (implementando más funcionalidades)
- Implementación de métodos para securizar la comunicación

## Problemas / Retos encontrados
- Comprensión de funcionamiento y uso de FastAPI
- Implementación de la persistencia de los datos

## Alternativas posibles
- Django REST Framework
- ASP.NET Web API
