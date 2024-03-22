import requests
import random
import time
from datetime import datetime

# Función que genera los datos sintéticos aleatoriamente
def generate_synthetic_data():
    # Generar producción energética aleatoria
    production = round(random.uniform(0, 5), 2)
    # Hacer que el resultado sea negativo con una probabilidad del 10%
    if random.random() < 0.1:
        production *= -1
    # Hacer que el resultado sea mayor que 5 con una probabilidad del 10%
    if random.random() < 0.1:
        production = round(production + random.uniform(5, 10), 2)
    
    return {
        "production": production,
        "state": bool(random.getrandbits(1)),
        "datetime": str(datetime.now())
        }


# Función principal
def main():
    while True:
        # Se repite para los 10 generadores
        for generator_id in range(1,11):
            # Obtiene los datos sintéticos
            data = generate_synthetic_data()
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


# Llamada a la función principal al iniciar el programa
if __name__ == "__main__":
    main()
