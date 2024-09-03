from flask import Flask, request, jsonify

app = Flask.__name__


@app.route('/registrar_incidente', methods=['POST'])
def registrar_incidente():
    pass


@app.route('/monitor', methods=['GET'])
def monitor_services():
    pass


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(port=5000)
