from flask import Flask, request, jsonify

app = Flask.__name__


@app.route('/validar_incidentes', methods=['POST'])
def validar_incidentes():
    pass


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(port=5002)
