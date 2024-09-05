import logging

from flask import Flask, jsonify

app = Flask(__name__)

logging.basicConfig(
    filename='../logs/manejador_incidentes.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def init_db():
  pass


init_db()


@app.route('/registrar_incidente', methods=['POST'])
def registrar_incidente():
  pass


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

