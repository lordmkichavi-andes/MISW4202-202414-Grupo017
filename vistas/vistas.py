import logging
from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from modelo.modelos import db, Incidente, IncidenteSchema

# Configurar el registro de logs
logging.basicConfig(
    filename='logs/validador_incidentes.log',  # Ruta al archivo de log
    level=logging.INFO,  # Nivel de registro
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato de los mensajes de log
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato de la fecha
)

# Inicialización del esquema de Incidente
incidente_schema = IncidenteSchema()


class VistaRegistrarIncidente(Resource):
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

    def post(self):
        # Validar que la solicitud contenga datos JSON
        if not request.is_json:
            logging.error("Solicitud fallida: La solicitud debe ser en formato JSON.")
            return {"error": "La solicitud debe ser en formato JSON"}, 400

        # Obtener los datos de la solicitud
        data = request.get_json()
        descripcion = data.get("descripcion")

        # Validar que la descripción esté presente
        if not descripcion:
            logging.error("Solicitud fallida: Falta la descripción del incidente.")
            return {"error": "Falta la descripción del incidente"}, 400

        # Crear un nuevo objeto Incidente
        nuevo_incidente = Incidente(descripcion=descripcion)

        # Intentar guardar el incidente en la base de datos
        try:
            db.session.add(nuevo_incidente)
            db.session.commit()
            logging.info(f"Incidente registrado exitosamente: {descripcion}")
            return {"mensaje": "Incidente registrado exitosamente",
                    "incidente": incidente_schema.dump(nuevo_incidente)}, 201
        except IntegrityError:
            db.session.rollback()
            logging.error(
                f"Error de integridad de datos al registrar el incidente: {descripcion}. Es posible que el incidente ya exista.")
            return {"error": "Error de integridad de datos. Es posible que el incidente ya exista."}, 409
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Error al registrar el incidente: {descripcion}. Detalles: {str(e)}")
            return {"error": f"Error al registrar el incidente: {str(e)}"}, 500
