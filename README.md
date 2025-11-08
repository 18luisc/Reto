Requisitos Previos

Tener instalados y configurados los siguientes componentes en el sistema:

*Docker Desktop: Con la función de Kubernetes habilitada y corriendo.
*kubectl: La herramienta de línea de comandos para interactuar con Kubernetes.
*cURL / Invoke-RestMethod: Para probar las APIs desde la terminal.
*Cuenta de Docker Hub: para subir la imagen de la aplicación.

Estructura del Proyecto:

├── postgres-pvc.yaml       # Define la solicitud de volumen persistente.
├── postgres-pod.yaml       # Define el Pod de PostgreSQL (BD).
├── postgres-service.yaml   # Define el Service para la BD.
├── app-deployment.yaml     # Define el Deployment y el Pod de la App.
├── app-service.yaml        # Define el Service para exponer la App.
└── app/
    ├── app.py              # Lógica de la aplicación Flask y conexión a BD.
    ├── requirements.txt    # Dependencias de Python (Flask, psycopg2-binary).
    └── Dockerfile          # Instrucciones para construir la imagen de la App.

# Entorno Virtual
1. python -m venv venv
2. .\venv\Scripts\activate

# Iniciar Minikube
minikube start

