from flask import Flask, request, jsonify
import sqlite3
import logging
import threading


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../logs/manejador_incidentes.log"),
        logging.StreamHandler()
    ]
)



def init_db():
    conn = sqlite3.connect('incidentes.db', check_same_thread=False)  # Permitir uso en múltiples hilos
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incidentes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT, severidad TEXT)''')
    conn.commit()
    conn.close()



def create_app():
    app = Flask(__name__)

    @app.route('/registrar_incidente', methods=['POST'])
    def registrar_incidente():
        """Registrar un incidente en la base de datos"""
        incidente = request.json
        if not incidente or not incidente.get('descripcion'):
            logging.error("Datos del incidente faltantes")
            return jsonify({"status": "error", "message": "Datos del incidente faltantes"}), 400

        try:
            conn = sqlite3.connect('incidentes.db', check_same_thread=False)  # Permitir uso en múltiples hilos
            cursor = conn.cursor()
            cursor.execute("INSERT INTO incidentes (descripcion, severidad) VALUES (?, ?)",
                           (incidente['descripcion'], incidente.get('severidad', 'media')))
            conn.commit()
            incidente_id = cursor.lastrowid
            conn.close()
            logging.info(f"Incidente registrado en la BD con ID {incidente_id}")  # Log cuando se registra correctamente
            return jsonify({"status": "success", "id": incidente_id}), 200
        except Exception as e:
            logging.error(f"Error al registrar incidente en la BD: {str(e)}")
            return jsonify({"status": "error", "message": "Error al registrar incidente"}), 500

    @app.route('/health', methods=['GET'])
    def health():
        """Endpoint para verificar la salud del microservicio"""
        logging.info("Chequeo de salud ejecutado")
        return jsonify({"status": "healthy"}), 200

    return app



def run_app_instance(port):
    app = create_app()
    app.run(port=port, debug=True, use_reloader=False)


if __name__ == '__main__':

    init_db()


    logging.info("Iniciando el servicio de manejador de incidentes")

    # Ejecutar tres instancias de la aplicación Flask en diferentes puertos
    ports = [5001, 5002, 5003]
    threads = []

    for port in ports:
        thread = threading.Thread(target=run_app_instance, args=(port,))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()