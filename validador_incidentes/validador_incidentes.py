from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='../logs/validador_incidentes.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@app.route('/validar_incidentes', methods=['POST'])
def validar_incidentes():
    pass

