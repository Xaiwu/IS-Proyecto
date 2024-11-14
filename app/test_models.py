from . import create_app, db
from app.models import Especialista, Paciente, Cita

app = create_app()

with app.app_context():
    # Crear la base de datos y las tablas
    db.create_all()

    # Insertar un especialista
    especialista = Especialista(
        nombre='Dr. Juan Pérez', especialidad='Cardiología')
    db.session.add(especialista)
    db.session.commit()

    # Insertar un paciente
    paciente = Paciente(nombre='Ana Gómez',
                        telefono='123456789', direccion='Calle Falsa 123')
    db.session.add(paciente)
    db.session.commit()

    # Insertar una cita
    cita = Cita(fecha='2024-11-12', hora='10:00',
                id_especialista=especialista.id, id_paciente=paciente.id)
    db.session.add(cita)
    db.session.commit()

    # Consultar los datos
    especialistas = Especialista.query.all()
    pacientes = Paciente.query.all()
    citas = Cita.query.all()

    print('Especialistas:', especialistas)
    print('Pacientes:', pacientes)
    print('Citas:', citas)
