import logging

from flask import Flask, request, jsonify
import requests
import threading

app = Flask.__name__

# Configurar el registro de logs
logging.basicConfig(
    filename='logs/api_gateway.log',  # Ruta al archivo de log
    level=logging.INFO,  # Nivel de registro
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato de los mensajes de log
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato de la fecha
)

"""
   POST /registrar_incidente
   Registrar un nuevo incidente.

   Cuerpo de la solicitud (JSON):
       - descripcion (str): Descripción del incidente.

   Respuesta:
       201 Created: Retorna el incidente creado en formato JSON.
       400 Bad Request: Si falta la descripción del incidente.
       500 Internal Server Error: Si ocurre un error al intentar registrar el incidente en la base de datos.
"""


@app.route('/registrar_incidente', methods=['POST'])
def registrar_incidente():
    registro = requests.post(f"http://registro:5001/registrar_incidente", request.get_json())
    if registro.status_code == 200:
        return jsonify(registro.json()), 200
    else:
        return {"error": "No se pudo registrar el incidente"}, 400


@app.route('/monitor', methods=['GET'])
def monitor_services():
    services = {
        {'nombre': 'manejador', 'puerto': 5001, },
        {'nombre': 'validador', 'puerto': 5002, }
    }
    for service in services:
        registro = requests.post(f"http://registro:{str(service['puerto'])}/health")

        if registro.status_code != 200:
            logging.error(f"Error en el servicio {service['nombre']}.")


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


def timer(timer_runs):
    # (4) El código corre mientras el booleano sea verdadero.
    while timer_runs.is_set():
        monitor_services()
        time.sleep(300)  # 5 minutos.


if __name__ == '__main__':
    app.run(port=5000)

    # (1) Creación del booleano que indica si el hilo secundario
    # debe correr o no.
    timer_runs = threading.Event()
    # (2) Iniciarlo con el valor True.
    timer_runs.set()
    # (3) Pasarlo como argumento al timer para que pueda leerlo.
    t = threading.Thread(target=timer, args=(timer_runs,))
    t.start()
