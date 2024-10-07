import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random
import string

import bcrypt

from dotenv import load_dotenv
import os

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