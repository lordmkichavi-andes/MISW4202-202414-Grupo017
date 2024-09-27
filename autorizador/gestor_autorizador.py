import os
import jwt
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'abcall.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    nombre= db.Column(db.String(80), nullable=False)
    direccion= db.Column(db.String(80), nullable=False)

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    nombre = data['nombre']
    direccion = data['direccion']

    if Usuario.query.filter_by(username=username).first():
        return jsonify({'message': 'El usuario ya existe!'}), 409

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = Usuario(username=username, password_hash=hashed_password, nombre=nombre, direccion=direccion)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente!'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = Usuario.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Credenciales inválidas!'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 200

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token faltante!'}), 403
    try:
        token = token.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({'message': 'Token válido!', 'user_id': data['user_id']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'El token ha expirado!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido!'}), 403

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    cert_path = os.path.join(base_dir, '..', 'certificados', 'cert.pem')
    key_path = os.path.join(base_dir, '..', 'certificados', 'key_sin_frase.pem')
    app.run(ssl_context=(cert_path, key_path), host='0.0.0.0', port=5001)
