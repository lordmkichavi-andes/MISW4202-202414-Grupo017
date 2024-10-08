from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from manejador_incidentes.vistas import VistaRegistrarIncidente
from modelo.modelos import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidentes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
cors = CORS(app)
api = Api(app)
api.add_resource(VistaRegistrarIncidente, '/registrar_incidente')

