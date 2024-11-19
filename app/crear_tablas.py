from app import create_app, db
from app.models import Especialista, Paciente, Cita

app = create_app()

with app.app_context():
    db.create_all()  # Esto creará todas las tablas definidas en tus modelos
