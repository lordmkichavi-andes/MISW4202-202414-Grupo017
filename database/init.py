
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance', 'abcall.db'))
print(f"Ruta de la base de datos: {db_path}")


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()
    print("Base de datos y tabla 'Usuario' creadas exitosamente.")

