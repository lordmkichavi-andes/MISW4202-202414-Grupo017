from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()
# Modelo de Incidente
class Incidente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(128), nullable=False)
    estado = db.Column(db.Boolean, default=True)


# Esquema de Incidente para serialización/deserialización
class IncidenteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incidente
        include_relationships = True
        load_instance = True


incidente_schema = IncidenteSchema()
incidentes_schema = IncidenteSchema(many=True)


