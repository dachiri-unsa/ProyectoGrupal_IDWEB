import mysql.connector

def get_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="BD_IDWEB_grupal"
    )
    return conexion

def crear_usuario(gmail, nombre, contrasenia, recibir_correos):
    conn = get_conexion()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO usuarios (gmail, nombre, contrasenia, recibir_correos)
            VALUES (%s, %s, %s, %s)
        """
        # recibir_correos es tinyint(1), aseguramos que sea 0 o 1
        val_recibir = 1 if recibir_correos else 0
        cursor.execute(sql, (gmail, nombre, contrasenia, val_recibir))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("Error al crear usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def leer_usuario(gmail):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM usuarios WHERE gmail = %s"
        cursor.execute(sql, (gmail,))
        usuario = cursor.fetchone()
        return usuario
    except Exception as e:
        print("Error al obtener usuario:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def validar_usuario(gmail, contrasenia):
    usuario = leer_usuario(gmail)
    if usuario and usuario['contrasenia'] == contrasenia:
        return usuario
    return None

def leer_usuarios():
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def actualizar_usuario(gmail, nombre, contrasenia, recibir_correos):
    conn = get_conexion()
    cursor = conn.cursor()
    try:
        sql = """
            UPDATE usuarios
            SET nombre = %s,
                contrasenia = %s,
                recibir_correos = %s
            WHERE gmail = %s
        """
        val_recibir = 1 if recibir_correos else 0
        cursor.execute(sql, (nombre, contrasenia, val_recibir, gmail))
        conn.commit()

        if cursor.rowcount == 0:
            raise Exception(f"No existe usuario con gmail {gmail}")

        return True
    except Exception as e:
        print("Error al actualizar usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def borrar_usuario(gmail):
    conn = get_conexion()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM usuarios WHERE gmail = %s"
        cursor.execute(sql, (gmail,))
        conn.commit()

        if cursor.rowcount == 0:
            raise Exception(f"No existe usuario con gmail {gmail}")

        return True
    except Exception as e:
        print("Ocurrió un error al eliminar usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()
