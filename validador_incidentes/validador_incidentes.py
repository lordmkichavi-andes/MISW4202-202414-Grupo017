from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='../logs/validador_incidentes.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def validar_respuestas(respuestas):
    if len(respuestas) == 0:
        return {"status": "error", "message": "No se recibieron respuestas para validar"}

    respuestas_exitosas = [resp for resp in respuestas if resp['status'] == 'success']
    respuestas_errores = [resp for resp in respuestas if resp['status'] == 'error']

    if len(respuestas_exitosas) == 0:
        logging.error("Todas las respuestas tienen errores")
        return {"status": "error", "message": "Todas las respuestas tienen errores", "detalles": respuestas_errores}

    if len(respuestas_exitosas) > 1:
        respuestas_mayoritarias = [r['incidente'] for r in respuestas_exitosas]
        
        resultado_mayoritario = max(set(respuestas_mayoritarias), key=respuestas_mayoritarias.count)
        
        return {"status": "success", "message": "Incidente validado por mayoría", "resultado": resultado_mayoritario}
    

    return {"status": "success", "message": "Incidente validado", "resultado": respuestas_exitosas[0]}


@app.route('/validar_incidentes', methods=['POST'])
def validar_incidentes():
    try:
        respuestas = request.json["respuestas"]

        resultado = validar_respuestas(respuestas)

        if resultado['status'] == 'success':
            logging.info(f"Incidente validado correctamente: {resultado['message']}")
        else:
            logging.error(f"Error al validar incidente: {resultado['message']}")

        return jsonify(resultado), 200
    except Exception as e:
        logging.error(f"Error en el proceso de validación: {str(e)}")
        return jsonify({"status": "error", "message": "Error en el proceso de validación"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(port=5004, debug=True)
