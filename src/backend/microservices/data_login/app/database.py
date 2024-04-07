import mysql.connector
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME
from mysql.connector import Error, errorcode
from jose import jwt
from typing import Optional
from datetime import datetime
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from passlib.context import CryptContext
from datetime import timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Función para conectar a la base de datos
def connect_to_database():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)

def create_user(db, user):
    # Verificar si el usuario ya existe
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (user.email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"error": "User already exists."}

        # Insertar el nuevo usuario si no existe
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        values = (user.username, user.email, user.password)  # Asegúrate de que password ya esté hasheado
        cursor.execute(query, values)
        db.commit()  # Guardar los cambios
        user_id = cursor.lastrowid  # Obtener el ID del nuevo usuario

        return {"user_id": user_id, "username": user.username, "email": user.email}

    except Error as e:
        print(f"Error al insertar el usuario en la base de datos: {e}")
        db.rollback()  # Revertir cambios en caso de error
        return {"error": "An error occurred while inserting the user into the database."}

    finally:
        if db.is_connected():
            cursor.close()

def close_db_connection(connection):
    connection.close()



def authenticate_user(email: str, password: str):
    db = connect_to_database()
    if db is None:
        return False
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and pwd_context.verify(password, user['password_hash']):
            return user
    finally:
        close_db_connection(db)
    return False

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data: dict):
    return create_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))