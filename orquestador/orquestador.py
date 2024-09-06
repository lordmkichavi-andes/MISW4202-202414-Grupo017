import requests
import logging
import time
import random
import json
import subprocess
from datetime import datetime, timedelta

logging.basicConfig(
    filename='../MISW4202-202414-Grupo017/logs/experimento_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

API_GATEWAY_URL = "http://localhost:5000"
MANEJADOR_URLS = [
    {'url': "http://localhost:5001/registrar_incidente", 'puerto': 5001},
    {'url': "http://localhost:5002/registrar_incidente", 'puerto': 5002},
    {'url': "http://localhost:5003/registrar_incidente", 'puerto': 5003},
]

VALIDADOR_URL = f"{API_GATEWAY_URL}/validar_incidentes"
MONITOR_URL = f"{API_GATEWAY_URL}/monitor"
API_GATEWAY_MANEJADOR = API_GATEWAY_URL + "/registrar_incidente"

def iniciar_microservicios():
    servicios = [
        ("python3", "api_gateway.py", "5000"),
        ("python3", "manejador_incidentes.py", "5001"),
        ("python3", "manejador_incidentes.py", "5002"),
        ("python3", "manejador_incidentes.py", "5003"),
        ("python3", "validador_incidentes.py", "5004")
    ]

    procesos = []
    for servicio in servicios:
        proceso = subprocess.Popen(
            ["python3", servicio[1], "--port", servicio[2]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        procesos.append(proceso)
        logging.info(f"Servicio {servicio[1]} iniciado en el puerto {servicio[2]}")

    return procesos

def detener_microservicios(procesos):
    for proceso in procesos:
        proceso.terminate()
        logging.info(f"Servicio {proceso.args} detenido")

def monitorear_servicios():
    try:
        response = requests.get(MONITOR_URL)
        if response.status_code == 200:
            logging.info(f"Estado de los servicios: {response.json()}")
            return response.json()
        else:
            logging.warning(f"Problema en el monitoreo de servicios: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Excepción al monitorear servicios: {str(e)}")
        return None

def registrar_incidente_con_datos(incident_data, es_fallido=False, reintentos=3):
    respuestas = []
    for manejador in MANEJADOR_URLS:
        intento = 0
        while intento < reintentos:
            if es_fallido:
                incident_data['descripcion'] = ""
                logging.info(f"Simulando datos fallidos en {manejador['url']}")

            try:
                incident_data['puerto'] = manejador['puerto']
                response = requests.post(API_GATEWAY_MANEJADOR, json=incident_data)
                if response.status_code == 200:
                    logging.info(f"Incidente registrado correctamente en {manejador['url']}")
                    respuestas.append("success")
                    break
                else:
                    logging.warning(f"Error al registrar incidente en {manejador['url']}: {response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Excepción al registrar incidente en {manejador['url']}: {str(e)}")
            intento += 1
            if intento < reintentos:
                logging.info(f"Reintentando registro en {manejador['url']} (Intento {intento + 1})...")
                time.sleep(2)
        if intento == reintentos:
            respuestas.append("error")
    return respuestas

def validar_respuestas(respuestas):
    try:
        response = requests.post(VALIDADOR_URL, json={"respuestas": respuestas})
        if response.status_code == 200:
            resultado = response.json().get("resultado")
            logging.info(f"Resultado de la validación de incidentes: {resultado}")
            return resultado
        else:
            logging.error(f"Error en la validación de respuestas: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Excepción al validar respuestas: {str(e)}")
        return None

def ejecutar_experimento(repeticiones=60, duracion_minutos=5, probabilidad_fallas=0.3):
    procesos = iniciar_microservicios()
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duracion_minutos)
    resultados = []

    for i in range(repeticiones):
        logging.info(f"Iniciando iteración {i + 1} del experimento.")
        estado_servicios = monitorear_servicios()
        es_fallido = random.random() < probabilidad_fallas
        if estado_servicios and estado_servicios.get("status") == "healthy":
            incident_data = {"descripcion": f"Incidente {i + 1}", "severidad": "alta"}
            respuestas = registrar_incidente_con_datos(incident_data, es_fallido)
            resultado = validar_respuestas(respuestas)
            if resultado == "success":
                logging.info(f"Experimento exitoso en la iteración {i + 1}.")
                resultados.append("success")
            else:
                logging.error(f"Fallos detectados en la iteración {i + 1}.")
                resultados.append("error")
        else:
            logging.warning("Saltando iteración debido a problemas de salud en los servicios.")
            resultados.append("error")

        time.sleep(10)

    generar_resumen_experimento(resultados)
    guardar_resultados(resultados)
    detener_microservicios(procesos)

def generar_resumen_experimento(resultados):
    total_intentos = len(resultados)
    exitosos = resultados.count("success")
    fallos = resultados.count("error")
    logging.info(f"Resumen del experimento: {exitosos}/{total_intentos} intentos exitosos, {fallos} fallos.")
    print(f"Resumen del experimento: {exitosos}/{total_intentos} intentos exitosos, {fallos} fallos.")

def guardar_resultados(resultados):
    with open('resultados_experimento.json', 'w') as archivo:
        json.dump(resultados, archivo)
    logging.info("Resultados guardados en resultados_experimento.json")


if __name__ == '__main__':
    ejecutar_experimento(repeticiones=60, duracion_minutos=5, probabilidad_fallas=0.3)
