import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(fecha, hora, nombre_paciente, email_paciente):
    
    # Configuración del servidor y credenciales
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'tu_email@gmail.com'
    sender_password = 'tu_contraseña'

    # Crear el mensaje
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_paciente
    message['Subject'] = 'Recordatorio de cita médica'
    body = f'Hola {nombre_paciente},\n\nTe recordamos que tienes una cita médica el día {fecha} a las {hora}.\n\nSaludos.'

    # Agregar el cuerpo del mensaje
    message.attach(MIMEText(body, 'plain'))

    try:
        # Conexión al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Activar cifrado TLS
        server.login(sender_email, sender_password)  # Autenticación
        text = message.as_string()
        server.sendmail(sender_email, email_paciente, text)  # Enviar el correo
        print("Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()  # Cerrar la conexión
