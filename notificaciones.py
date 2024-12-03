import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Si modificas estos alcances, elimina el archivo token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def enviar_correo(fecha, hora, nombre_paciente, email_paciente):
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si no hay credenciales válidas disponibles, permite al usuario iniciar sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)  # Asegúrate de que el puerto coincide con el configurado en Google Cloud
        # Guarda las credenciales para la próxima ejecución.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Crear el mensaje
    message = MIMEMultipart()
    message['From'] = 'tu_correo@gmail.com'
    message['To'] = email_paciente
    message['Subject'] = 'Recordatorio de cita médica'
    body = f'Hola {nombre_paciente},\n\nTe recordamos que tienes una cita médica el día {fecha} a las {hora}.\n\nSaludos.'
    message.attach(MIMEText(body, 'plain'))

    # Convertir el mensaje a base64
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Crear el servicio de la API de Gmail
    service = build('gmail', 'v1', credentials=creds)

    # Crear el cuerpo del mensaje
    message_body = {
        'raw': raw
    }

    try:
        # Enviar el correo
        message = service.users().messages().send(userId='me', body=message_body).execute()
        print(f"Correo enviado exitosamente! ID del mensaje: {message['id']}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# enviar_correo('2024-12-12', '10:00', 'Vicente ramirez', 'vicramirez2022@udec.cl')