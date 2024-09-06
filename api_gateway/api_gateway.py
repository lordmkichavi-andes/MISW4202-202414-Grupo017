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

MANEJADOR_URLS = {
    5001: "http://localhost:5001/registrar_incidente",
    5002: "http://localhost:5002/registrar_incidente",
    5003: "http://localhost:5003/registrar_incidente"
}
VALIDADOR_URL = "http://localhost:5004/validar_incidentes"
MONITOR_URLS = [
    "http://localhost:5001/health",
    "http://localhost:5002/health",
    "http://localhost:5003/health"
]

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
    incidente = {"descripcion": f"Incidente {request.json['descripcion']}", "severidad": {request.json['severidad']}}
    puerto = request.json['puerto']
    registro = requests.post(MANEJADOR_URLS[puerto], incidente)

    if registro.status_code == 200:
        logging.info(f"Incidente registrado correctamente en {MANEJADOR_URLS[puerto]})

        return jsonify(registro.json()), 200
    else:
        logging.info(f"Excepción al registrar incident en {MANEJADOR_URLS[puerto]})

        return {"error": "No se pudo registrar el incidente"}, 400

@app.route('/validar_incidentes', methods=['POST'])
def validar_incidentes():
    respuesta = requests.post(VALIDADOR_URL, request.get_json())
    if registro.status_code == 200:
        logging.info(f"Incidente validado correctamente en {VALIDADOR_URL})

        return jsonify(registro.json()), 200
    else:
        logging.info(f"Excepción al validar incident en {VALIDADOR_URL})

        return {"error": "No se pudo validar el incidente"}, 400

@app.route('/monitor', methods=['GET'])
def monitor_services():
    estado_Servicios = []
    for manejador in MANEJADOR_URLS:
        registro = requests.post(f"{manejador}/health")

        estado_Servicios.append(registrar_estado_Servicios(registro.status_code,service['nombre']))

    registro = requests.post(f"{VALIDADOR_URL}/health")
    estado_Servicios.append(registrar_estado_Servicios(registro.status_code, VALIDADOR_URL))

    return jsonify(estado_Servicios), 200


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200




def registrar_estado_Servicios(status_code: int, servicio: str):
    if status_code != 200:
        logging.error(f"Error en el servicio {servicio}.")
        return {manejador, 'Fallando'}
    return {manejador, 'Funcionando'}

if __name__ == '__main__':
    app.run(port=5000)