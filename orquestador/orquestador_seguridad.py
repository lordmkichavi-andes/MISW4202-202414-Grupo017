import logging
import threading

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_GATEWAY_URL = 'https://localhost:5010'

USERNAME = 'lucho'
PASSWORD = 'Luchi2020*'


def authenticate(username, password):
    url = f'{API_GATEWAY_URL}/api/auth/login'
    payload = {
        'username': username,
        'password': password
    }
    logger.info(f'Autenticando usuario {username}...')
    try:
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()
        token = response.json().get('token')
        logger.info(f'Autenticado con éxito. Token: {token}')
        return token
    except requests.exceptions.RequestException as e:
        logger.error(f'Error en la autenticación: {e}')
        return None


def modificar_datos_personales(token, datos):
    url = f'{API_GATEWAY_URL}/api/clients/update'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    logger.info('Modificando datos personales del cliente...')
    response = requests.put(url, json=datos, headers=headers)

    if response.status_code == 200:
        logger.info('Datos personales modificados con éxito.')
    else:
        logger.error(f'Error al modificar los datos personales: {response.status_code}')


def intentar_violacion_de_seguridad(intercepted_token, datos):
    logger.warning('Intentando modificar los datos personales con un token interceptado...')
    modificar_datos_personales(intercepted_token, datos)


def usar_token_expirado(datos):
    expired_token = "expired.jwt.token"
    logger.warning('Intentando modificar los datos personales con un token expirado...')
    modificar_datos_personales(expired_token, datos)


def usar_token_manipulado(datos):
    manipulated_token = "manipulated.jwt.token"
    logger.warning('Intentando modificar los datos personales con un token manipulado...')
    modificar_datos_personales(manipulated_token, datos)


def modificar_datos_simultaneamente(token, datos):
    def worker():
        modificar_datos_personales(token, datos)

    logger.info('Modificando datos simultáneamente desde dos sesiones...')
    thread1 = threading.Thread(target=worker)
    thread2 = threading.Thread(target=worker)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def modificar_datos_de_otro_usuario():
    token_otro_usuario = authenticate('cliente2', 'password2')
    datos_ajenos = {
        'nombre': 'Nombre Ajeno',
        'direccion': 'Dirección Ajenos'
    }
    logger.warning('Intentando modificar los datos de otro usuario...')
    modificar_datos_personales(token_otro_usuario, datos_ajenos)


def probar_conexion_no_segura(token, datos):
    url_http = API_GATEWAY_URL.replace('https', 'http')
    logger.warning('Intentando modificar los datos personales sin conexión segura (HTTP)...')
    modificar_datos_personales(token, datos)


def main():
    token = authenticate(USERNAME, PASSWORD)

    if token:
        datos_nuevos = {
            'nombre': 'luis gomez',
            'direccion': 'calle 8 sur'
        }

        modificar_datos_personales(token, datos_nuevos)

        intercepted_token = token
        intentar_violacion_de_seguridad(intercepted_token, datos_nuevos)

        usar_token_expirado(datos_nuevos)

        usar_token_manipulado(datos_nuevos)

        modificar_datos_simultaneamente(token, datos_nuevos)

        modificar_datos_de_otro_usuario()

        probar_conexion_no_segura(token, datos_nuevos)


if __name__ == '__main__':
    logger.info('Iniciando orquestador...')
    main()
