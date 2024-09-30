from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.init import db, Usuario 

app = Flask(__name__)

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'instance', 'abcall.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

base_dir = os.path.abspath(os.path.dirname(__file__))
cert_path = os.path.join(base_dir, '..', 'certificados', 'cert.pem')
key_path = os.path.join(base_dir, '..', 'certificados', 'key_sin_frase.pem')

db.init_app(app)

@app.route('/api/clients/update', methods=['PUT'])
def modificar_datos_personales():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token faltante!'}), 403

    try:
        token = token.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id'] 
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'El token ha expirado!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido!'}), 403

    id_modificacion = request.json.get('id', None)
    nombre = request.json.get("nombre", None)
    direccion = request.json.get("direccion", None)

    if not nombre or not direccion:
        return jsonify({"message": "Faltan datos para la actualización"}), 400

    if user_id != id_modificacion:
        return jsonify({'message': 'No está autorizado para modificar los datos de otro usuario'}), 403
        
    user = Usuario.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'Usuario no encontrado!'}), 404

    user.nombre = nombre
    user.direccion = direccion

    try:
        db.session.commit()
        return jsonify({'message': 'Datos personales actualizados con éxito!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar los datos personales', 'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(cert_path):
            print(f"El archivo de certificado no se encontró en la ruta: {cert_path}")
        if not os.path.exists(key_path):
            print(f"El archivo de clave privada no se encontró en la ruta: {key_path}")
        app.run(ssl_context=(cert_path, key_path), host='0.0.0.0', port=5002)
