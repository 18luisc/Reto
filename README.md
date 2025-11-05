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

A. Aplicar Configuración Inicial
Despliega el volumen persistente, el Pod de la BD y su Service.

# 1. Almacenamiento Persistente (PVC)
kubectl apply -f postgres-pvc.yaml

# 2. Pod de la Base de Datos (PostgreSQL)
kubectl apply -f postgres-pod.yaml

# 3. Service para la BD (Nombre de red interno: postgres-service)
kubectl apply -f postgres-service.yaml

B. Crear la Tabla productos
Esperamos hasta que el Pod postgres-db esté en estado Running (kubectl get pods).

# Entrar al Pod
kubectl exec -it postgres-db -- bash

# Conectarse al cliente (Contraseña: mypassword)
psql -U user -d appdb

# Ejecutar la creación de la tabla
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2)
);

# Salir
\q
exit

C. Construir y Subir la Imagen
Estar dentro de la carpeta app/ para construir la imagen.

# 1. Construir la imagen
docker build -t luceroluis/app-reto:v2 .

# 2. Subir al registro
docker push luceroluis/app-reto:v2

D. Actualizar y Desplegar en Kubernetes
Nos aseguramos de que app-deployment.yaml apunte a la imagen correcta (luceroluis/app-reto:v2)

# 1. Aplicar el Deployment (crea el Pod de la aplicación)
kubectl apply -f app-deployment.yaml

# 2. Aplicar el Service para acceso externo (localhost)
kubectl apply -f app-service.yaml

E. Creación de Registro (POST)
Usamos Invoke-RestMethod en PowerShell o curl en terminales basadas en Linux/Git Bash.

# Opción PowerShell (Windows)
Invoke-RestMethod -Uri "http://localhost/productos" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"nombre": "Mouse Gamer", "precio": 45.99}'
Respuesta esperada: {"mensaje": "Producto 'Mouse Gamer' creado con éxito"}

F. Consulta de Datos (GET)

# Opción PowerShell (Windows)
Invoke-RestMethod -Uri "http://localhost/productos" -Method GET
Respuesta esperada: Un listado JSON que incluye el registro creado.

G. Limpieza de Recursos

# Para liberar el almacenamiento
kubectl delete deployment app-deployment
kubectl delete service app-frontend
kubectl delete service postgres-service
kubectl delete pod postgres-db
kubectl delete pvc postgres-pv-claim