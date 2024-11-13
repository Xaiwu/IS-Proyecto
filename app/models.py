# Se definiran clases que representan las tablas de la base de datos
from . import db


class Especialista(db.Model):
    __tablename__ = 'especialistas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship(
        'Usuario', backref=db.backref('especialista', uselist=False))

    def __repr__(self):
        return f'<Especialista {self.id} - {self.nombre} - {self.especialidad}>'


class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship(
        'Usuario', backref=db.backref('paciente', uselist=False))

    def __repr__(self):
        return f'<Paciente {self.id} - {self.nombre} - {self.telefono}>'


class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    id_especialista = db.Column(db.Integer, db.ForeignKey('especialistas.id'))
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'))
    especialista = db.relationship(
        'Especialista', backref=db.backref('citas', lazy=True))
    paciente = db.relationship(
        'Paciente', backref=db.backref('citas', lazy=True))

    def __repr__(self):
        return f'<Cita {self.id} - {self.fecha} - {self.hora} - Especialista {self.id_especialista} - Paciente {self.id_paciente}>'
