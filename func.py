import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random
import string

import bcrypt

from google.cloud.sql.connector import Connector
connector = Connector()

from dotenv import load_dotenv
import os
import re

load_dotenv()

def enviar_email(reciber,cod):
    email_sender = os.environ['EMAIL']
    password = os.environ['PASS']
    email_reciber = reciber
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_reciber
    message['Subject'] = "Verificación"
    body = f"Hola, este es tu código de verificación: {cod}"
    message.attach(MIMEText(body,'plain'))
    smtp_server = smtplib.SMTP('smtp.gmail.com',587)
    smtp_server.starttls()
    smtp_server.login(email_sender,password)
    smtp_server.sendmail(email_sender,email_reciber,message.as_string())
    smtp_server.quit()


def generar_codigo(longitud=6):
    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
    return codigo

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def existe_usuario_correo(user,email):
    conn = connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"]
        )
    cursor = conn.cursor()
    cursor.execute(f'''SELECT usuario FROM public.usuarios WHERE usuario ='{user}' or email = '{email}' ''')
    result = cursor.fetchall()
    if len(result) == 0:
        return False ## No existe
    else:
        return True ## Existe

def consultar_contra(user,contra):
    conn = connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"]
        )
    cursor = conn.cursor()
    cursor.execute(f'''SELECT password FROM public.usuarios WHERE usuario ='{user}'  ''')
    result = cursor.fetchall()
    if len(result) ==0:
        return False
    else:
        return verify_password(contra,result[0][0]) ## True, False

def guardar_usuario(us,pa,em,fc):
    conn = connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"]
        )
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO public.usuarios (usuario, password, email, fecha_cre)
        VALUES (%s, %s, %s, %s)
    """
    data_to_insert = (us, hash_password(pa), em, fc)
    cursor.execute(insert_query, data_to_insert)
    conn.commit()
    cursor.close()
    conn.close() 

def modificar_password(email,pass_nuevo):
    conn = connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"]
        )
    cursor = conn.cursor()
    update_query = f"""
        UPDATE public.usuarios
        SET password = %s
        WHERE email = %s
    """
    new_password = hash_password(pass_nuevo)
    email_to_update = email
    cursor.execute(update_query, (new_password, email_to_update))
    conn.commit()
    cursor.close()
    conn.close()

def guardar_data(datos):
    conn = connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"]
        )
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO public.datos 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data_to_insert = datos
    cursor.execute(insert_query, data_to_insert)
    conn.commit()
    cursor.close()
    conn.close()


def guardar_data2(datos):
    # Conexión a la base de datos
    conn = connector.connect(
        os.environ["INSTANCE_CONNECTION_NAME"],
        "pg8000",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        db=os.environ["DB_NAME"]
    )
    cursor = conn.cursor()

    # Definición de la consulta de inserción con el número correcto de marcadores de posición
    insert_query = """
        INSERT INTO public.datos 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Contar cuántos parámetros se esperan
    expected_param_count = insert_query.count('%s')

    # Rellenar con None si hay menos parámetros de los esperados
    data_to_insert = list(datos) + [None] * (expected_param_count - len(datos))

    # Comprobar que no se exceda el número de parámetros
    if len(data_to_insert) > expected_param_count:
        print(f"Error: Se esperaban máximo {expected_param_count} parámetros, pero se proporcionaron {len(datos)}.")
        return

    # Inserción de datos en la base de datos
    try:
        cursor.execute(insert_query, data_to_insert)
        conn.commit()
    except Exception as e:
        print(f"Ocurrió un error al insertar datos: {e}")
        conn.rollback()  # Revertir en caso de error
    finally:
        cursor.close()
        conn.close()


def es_correo_valido(correo):
    # Expresión regular para validar el formato del correo
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo)
