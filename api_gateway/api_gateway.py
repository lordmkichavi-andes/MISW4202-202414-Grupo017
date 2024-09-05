from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='../logs/api_gateway.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MANEJADOR_URLS = [
    "http://localhost:5001/registrar_incidente",
    "http://localhost:5002/registrar_incidente",
    "http://localhost:5003/registrar_incidente"
]
VALIDADOR_URL = "http://localhost:5004/validar_incidentes"
MONITOR_URLS = [
    "http://localhost:5001/health",
    "http://localhost:5002/health",
    "http://localhost:5003/health"
]

@app.route('/monitor', methods=['GET'])
def monitor():
    pass


@app.route('/registrar_incidente', methods=['POST'])
def reenviar_registro_incidente():
    pass
