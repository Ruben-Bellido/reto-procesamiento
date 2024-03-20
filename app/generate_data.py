import requests
import random
import time
from datetime import datetime

# Genera los datos sintéticos aleatoriamente
def generate_synthetic_data(generator_id, measure_id):
    # Generar producción energética aleatoria
    production = round(random.uniform(0, 5), 2)
    # Hacer que el resultado sea erróneo con una probabilidad del 10%
    if random.random() < 0.1:
        production *= -1
    
    return {
        "generator_id": generator_id,
        "location": {
            "latitude": round(-1.11 * generator_id, 6),
            "longitude": round(1.11 * generator_id, 6)
            },
        "measure": {
            measure_id: {
                "production": production,
                "state": bool(random.getrandbits(1)),
                "datetime": str(datetime.now())
                }
            }
        }


# Función principal
def main():
    i = 0
    while True:
        # Se repite para los 10 generadores
        for generator_id in range(1,11):
            # Obtiene los datos sintéticos
            data = generate_synthetic_data(generator_id, i)
            # Debug para visualizar los datos
            print(f"Enviando datos: {data}")
            
            try:
                # URL del endpoint FastAPI
                url = f"http://127.0.0.1:8000/generators/{generator_id}" 
                # Envía la petición POST con los datos
                response = requests.post(url, json=data)
                # Debug para comprobar el estado de la petición
                if response.status_code == 200:
                    print("Petición POST exitosa")
                else:
                    print(f"Error en la petición POST. Código de estado: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error en la conexión: {e}")

        # Espera 10 segundos antes de generar nuevos datos
        time.sleep(10)  
        i += 1


if __name__ == "__main__":
    main()
