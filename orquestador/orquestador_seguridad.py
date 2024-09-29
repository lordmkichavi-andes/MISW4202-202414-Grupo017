import logging
import threading
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_GATEWAY_URL = 'https://localhost:5010'
API_GATEWAY_URL_HTTP = API_GATEWAY_URL.replace('https', 'http')  # URL HTTP para conexión no segura

USERNAME = 'lucho'
PASSWORD = 'Luchi2020*'


def authenticate(username, password, url_base):
    url = f'{url_base}/api/auth/login'
    payload = {
        'username': username,
        'password': password
    }
    logger.info(f'Autenticando usuario {username} en {url_base}...')
    try:
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()
        token = response.json().get('token')
        logger.info(f'Autenticado con éxito en {url_base}. Token: {token}')
        return token
    except requests.exceptions.RequestException as e:
        logger.error(f'Error en la autenticación en {url_base}: {e}')
        return None


def modificar_datos_personales(token, datos, url_base):
    url = f'{url_base}/api/clients/update'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    logger.info(f'Modificando datos personales del cliente en {url_base}...')
    try:
        response = requests.put(url, json=datos, headers=headers, verify=False)
        if response.status_code == 200:
            logger.info(f'Datos personales modificados con éxito en {url_base}.')
        else:
            logger.error(f'Error al modificar los datos personales en {url_base}: {response.status_code}')
    except requests.exceptions.ConnectionError as e:
        logger.error(f'Error de conexión al intentar modificar los datos personales en {url_base}: {e}')
    except requests.exceptions.RequestException as e:
        logger.error(f'Error general al intentar modificar los datos personales en {url_base}: {e}')



def intentar_violacion_de_seguridad(intercepted_token, datos, url_base):
    token_partes = intercepted_token.split('.')
    token_manipulado = token_partes[0] + '.' + token_partes[1] + '.' + 'interceptado'
    logger.warning(f'Intentando modificar los datos personales con un token interceptado en {url_base}...')
    modificar_datos_personales(token_manipulado, datos, url_base)


def usar_token_expirado(datos, url_base):
    expired_token = "expired.jwt.token"
    logger.warning(f'Intentando modificar los datos personales con un token expirado en {url_base}...')
    modificar_datos_personales(expired_token, datos, url_base)


def usar_token_manipulado(datos, url_base):
    manipulated_token = "manipulated.jwt.token"
    logger.warning(f'Intentando modificar los datos personales con un token manipulado en {url_base}...')
    modificar_datos_personales(manipulated_token, datos, url_base)


def modificar_datos_simultaneamente(token, datos, url_base):
    def worker():
        modificar_datos_personales(token, datos, url_base)

    logger.info(f'Modificando datos simultáneamente desde dos sesiones en {url_base}...')
    thread1 = threading.Thread(target=worker)
    thread2 = threading.Thread(target=worker)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def modificar_datos_de_otro_usuario(url_base):
    token_otro_usuario = authenticate('cliente2', 'password2', url_base)
    datos_ajenos = {
        'nombre': 'Nombre Ajeno',
        'direccion': 'Dirección Ajenos'
    }
    logger.warning(f'Intentando modificar los datos de otro usuario en {url_base}...')
    modificar_datos_personales(token_otro_usuario, datos_ajenos, url_base)


def probar_conexion_no_segura(token, datos):
    logger.warning('Intentando modificar los datos personales sin conexión segura (HTTP)...')
    modificar_datos_personales(token, datos, API_GATEWAY_URL_HTTP)

def probar_timeout(token, datos):
    logger.warning('Probando comportamiento de timeout...')
    try:
        response = requests.put(f'{API_GATEWAY_URL}/api/clients/update', json=datos, headers={'Authorization': f'Bearer {token}'}, timeout=0.001,  verify=False)
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout al intentar modificar los datos personales: {e}')


def probar_datos_malformados(token, url_base):
    logger.warning('Probando manejo de datos malformados en la solicitud...')
    datos_malformados = "{'nombre': 'Nombre', 'direccion': 'Dirección}"
    try:
        response = requests.put(f'{url_base}/api/clients/update', data=datos_malformados,
                                headers={'Authorization': f'Bearer {token}'}, verify=False)
        if response.status_code == 400:
            logger.info('La aplicación manejó correctamente los datos malformados con un error 400.')
        else:
            logger.error(
                f'Error inesperado al manejar datos malformados: Código de estado {response.status_code}, Respuesta: {response.text}')
    except requests.exceptions.RequestException as e:
        logger.error(f'Error al enviar datos malformados: {e}')


def main():
    token = authenticate(USERNAME, PASSWORD, API_GATEWAY_URL)
    if token:
        datos_nuevos = {
            'nombre': 'luis gomez',
            'direccion': 'calle 8 sur'
        }
        datos_alterados = {
            'nombre': 'carlos melendez',
            'direccion': 'calle 4 norte'
        }
        modificar_datos_personales(token, datos_nuevos, API_GATEWAY_URL)
        intentar_violacion_de_seguridad(token, datos_alterados, API_GATEWAY_URL)
        usar_token_expirado(datos_alterados, API_GATEWAY_URL)
        usar_token_manipulado(datos_alterados, API_GATEWAY_URL)
        modificar_datos_simultaneamente(token, datos_alterados, API_GATEWAY_URL)
        modificar_datos_de_otro_usuario(API_GATEWAY_URL)
        probar_timeout(token, datos_alterados)
        probar_datos_malformados(token, API_GATEWAY_URL)
        probar_conexion_no_segura(token, datos_alterados)

if __name__ == '__main__':
    logger.info('Iniciando orquestador...')
    main()
