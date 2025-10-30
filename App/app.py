from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# --- Configuración de Conexión a la BD (usando el nombre del Service) ---
DB_HOST = "postgres-service"
DB_NAME = "appdb"
DB_USER = "user"
DB_PASS = "mypassword"
DB_PORT = "5432"

def get_db_connection():
    """Función para establecer la conexión a PostgreSQL."""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

# --- RUTA 1: CREACIÓN DE REGISTROS (POST) ---
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')

    if not nombre or not precio:
        return jsonify({"mensaje": "Faltan nombre o precio"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        insert_query = "INSERT INTO productos (nombre, precio) VALUES (%s, %s);"
        cursor.execute(insert_query, (nombre, precio))
        conn.commit()
        
        return jsonify({"mensaje": f"Producto '{nombre}' creado con éxito"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# --- RUTA 2: CONSULTA DE DATOS (GET) ---
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        select_query = "SELECT id, nombre, precio FROM productos ORDER BY id;"
        cursor.execute(select_query)
        
        productos = []
        for row in cursor.fetchall():
            # psycopg2 devuelve DECIMAL, lo convertimos a string para JSON
            productos.append({
                "id": row[0],
                "nombre": row[1],
                "precio": str(row[2]) 
            })
            
        return jsonify(productos)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    # Usar 0.0.0.0 es crucial para que la aplicación sea accesible DENTRO del Pod.
    app.run(host='0.0.0.0', port=5000)