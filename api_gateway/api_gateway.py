import logging

from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token

import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'


# Configurar el registro de logs
logging.basicConfig(
    filename='../logs/api_gateway.log',  # Ruta al archivo de log
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
    "http://localhost:5003/health",
    "http://localhost:5004/health"
]
AUTENTICADOR_URL = "http://localhost:5001/api/auth/login"

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
    incidente = {
        "descripcion": request.json['descripcion'],
        "severidad": request.json['severidad']
    }
    puerto = request.json['puerto']
    registro = requests.post(MANEJADOR_URLS[puerto], json=incidente)

    if registro.status_code == 200:
        logging.info(f"Incidente registrado correctamente en {MANEJADOR_URLS[puerto]}")
        return jsonify(registro.json()), 200
    else:
        logging.info(f"Excepción al registrar incidente en {MANEJADOR_URLS[puerto]}")
        return {"error": "No se pudo registrar el incidente"}, 400


@app.route('/validar_incidentes', methods=['POST'])
def validar_incidentes():
    respuesta = requests.post(VALIDADOR_URL, json=request.get_json())
    if respuesta.status_code == 200:
        logging.info(f"Incidente validado correctamente en {VALIDADOR_URL}")

        return jsonify(respuesta.json()), 200
    else:
        logging.info(f"Excepción al validar incident en {VALIDADOR_URL}")

        return {"error": "No se pudo validar el incidente"}, 400


@app.route('/monitor', methods=['GET'])
def monitor_services():
    respuesta = {"status": "healthy", "servicios": []}
    estado_servicios = []
    estado_activo = True
    for monitor in MONITOR_URLS:
        registro = requests.get(f"{monitor}")
        logging.info(f"Estado del servicio {monitor}: {registro.status_code}")
        estado_servicio = registrar_estado_servicios(registro.status_code, str(monitor))
        if estado_servicio[1] is False:
            estado_activo = False
        estado_servicios.append(estado_servicio)

    if estado_activo:
        respuesta["status"] = "healthy"
    else:
        respuesta["status"] = "unhealthy"
    respuesta["servicios"] = estado_servicios
    return jsonify(respuesta), 200


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/auth/login', methods=['POST'])
def login():
    respuesta = requests.post(AUTENTICADOR_URL, json=request.get_json())
    if respuesta.status_code == 200:
        logging.info(f"Usuario creado correctamente en {AUTENTICADOR_URL}")
        token_de_acceso = create_access_token(identity=respuesta.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}, 201
    else:
        return {"mensaje": "Error creando el usuario"}, 400

def registrar_estado_servicios(status_code: int, servicio: str):
    if status_code != 200:
        logging.error(f"Error en el servicio {servicio}.")
        return [servicio, False]
    return [servicio, True]


if __name__ == '__main__':
    app.run(port=5010)
