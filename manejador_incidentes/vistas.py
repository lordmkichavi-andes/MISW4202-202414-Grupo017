import logging
from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from modelo.modelos import db, Incidente, IncidenteSchema

logging.basicConfig(
    filename='logs/validador_incidentes.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

incidente_schema = IncidenteSchema()

class VistaRegistrarIncidente(Resource):

    def post(self):
        if not request.is_json:
            logging.error("Solicitud fallida: La solicitud debe ser en formato JSON.")
            return {"error": "La solicitud debe ser en formato JSON"}, 400

        data = request.get_json()
        descripcion = data.get("descripcion")

        if not descripcion:
            logging.error("Solicitud fallida: Falta la descripción del incidente.")
            return {"error": "Falta la descripción del incidente"}, 400

        nuevo_incidente = Incidente(descripcion=descripcion)

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
