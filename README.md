# Sistema de Gestión de Incidentes (Arquitectura de Microservicios)

Este proyecto implementa un sistema de gestión de incidentes basado en una arquitectura de microservicios. El sistema está diseñado para registrar y validar incidentes, y consta de varios microservicios, como el manejador de incidentes, validador de incidentes, un API Gateway y un orquestador.

## Tabla de Contenidos
- Descripción del Proyecto
- Arquitectura del Sistema
- Microservicios
  - Manejador de Incidentes
  - Validador de Incidentes
  - API Gateway
  - Orquestador
- Parámetros de Configuración
- Ejecución del Sistema
- Monitoreo y Logs
- Autor

## Descripción del Proyecto
Este sistema permite registrar y validar incidentes a través de múltiples microservicios, manteniendo una arquitectura resiliente que distribuye las solicitudes entre diferentes instancias del servicio. Además, se implementan mecanismos de validación y monitoreo para asegurar la correcta operación del sistema bajo diferentes escenarios de carga y fallos simulados.

## Arquitectura del Sistema
La arquitectura del sistema sigue el patrón de microservicios, donde cada componente se encarga de una funcionalidad específica:

- Manejador de Incidentes: Recibe, procesa y almacena los incidentes.
- Validador de Incidentes: Valida la integridad y consistencia de los incidentes registrados.
- API Gateway: Punto central de acceso para los servicios del sistema.
- Orquestador: Controla los experimentos y simula fallos en los microservicios para probar su resiliencia.

## Microservicios

### Manejador de Incidentes
Este microservicio se encarga de procesar y registrar incidentes en una base de datos SQLite. Se ejecutan múltiples instancias del servicio en diferentes puertos.

- Tecnología: Flask, SQLite, Logging
- Endpoints:
  - POST /registrar_incidente: Registra un nuevo incidente.
  - GET /health: Verifica el estado del servicio.

### Validador de Incidentes
Este microservicio recibe las respuestas de los manejadores de incidentes y las valida, utilizando un mecanismo de votación para decidir el resultado más confiable en caso de inconsistencias.

- Tecnología: Flask, Logging
- Endpoints:
  - POST /validar_incidentes: Valida las respuestas de los manejadores de incidentes.
  - GET /health: Verifica el estado del servicio.

### API Gateway
El API Gateway actúa como un intermediario entre los clientes y los microservicios, distribuyendo las solicitudes a las instancias del manejador de incidentes y coordinando la validación de los mismos.

- Tecnología: Flask, Requests, Logging
- Endpoints:
  - POST /registrar_incidente: Distribuye las solicitudes de registro a los manejadores de incidentes.
  - POST /validar_incidentes: Envía las respuestas para validación.
  - GET /monitor: Verifica el estado de los servicios a través del monitoreo de sus endpoints de salud.

### Orquestador
El orquestador coordina la ejecución de experimentos para simular diferentes niveles de fallos y cargas, monitoreando los servicios involucrados y generando reportes de los resultados.

- Tecnología: Python, Requests, Logging
- Funciones:
  - ejecutar_experimento(): Simula la ejecución de múltiples incidentes, fallos y validaciones.

## Parámetros de Configuración
El sistema permite configurar varios parámetros para adaptar el comportamiento de los microservicios y los experimentos:

- Número de repeticiones: Define cuántas veces se ejecuta un experimento.
- Duración del experimento: Define cuánto tiempo durará cada experimento.
- Probabilidad de fallos: Ajusta la probabilidad de que un incidente falle al registrarse, simulando fallos en los servicios.

Estos parámetros se pueden ajustar directamente en el archivo `orquestador.py`.

## Ejecución del Sistema
Para ejecutar el sistema, sigue estos pasos:

1. Iniciar el Manejador de Incidentes:

   - `python manejador_incidentes.py`

   Esto levantará tres instancias del manejador de incidentes en los puertos 5001, 5002 y 5003.

2. Iniciar el Validador de Incidentes:

   - `python validador_incidentes.py`

3. Iniciar el API Gateway:

   - `python api_gateway.py`

4. Iniciar el Orquestador: El orquestador puede ejecutar experimentos configurados previamente:

   - `python orquestador.py`

## Monitoreo y Logs
Los servicios generan logs de sus actividades en la carpeta `logs/`. Los principales logs disponibles incluyen:

- **manejador_incidentes.log**: Registra las actividades y errores del servicio de manejo de incidentes.
- **validador_incidentes.log**: Contiene los registros de validación de incidentes.
- **api_gateway.log**: Registra las solicitudes entrantes al API Gateway y sus respuestas.
- **experimento_logs.log**: Detalla los resultados de los experimentos ejecutados por el orquestador.

## Autor
Proyecto desarrollado por Joyce Blanco, Margarita Villafañe, Andres Renteria, Javier Fajardo.
