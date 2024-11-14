from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, TimeField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
                         DataRequired(), Length(min=2, max=100)])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    direccion = StringField('Dirección', validators=[Length(max=200)])
    correo = EmailField('Correo Electrónico', validators=[
                        DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[
                             DataRequired(), Length(min=6)])
    rol = SelectField('Rol', choices=[('paciente', 'Paciente'), ('especialista',
                      'Especialista'), ('asistente', 'Asistente')], validators=[DataRequired()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    correo = EmailField('Correo Electrónico', validators=[
                        DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[
                             DataRequired(), Length(min=6)])
    submit = SubmitField('Iniciar Sesión')


class ReservaForm(FlaskForm):
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    hora = SelectField('Hora', coerce=str, validators=[DataRequired()])
    especialista = SelectField(
        'Especialista', coerce=int, validators=[DataRequired()])
    paciente = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Reservar/Modificar')


class AsistenteReservaForm(FlaskForm):
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    hora = SelectField('Hora', coerce=str, validators=[DataRequired()])
    especialista = SelectField(
        'Especialista', coerce=int, validators=[DataRequired()])
    paciente = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Reservar/Modificar')


class PacienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
                         DataRequired(), Length(min=2, max=100)])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    direccion = StringField('Dirección', validators=[Length(max=200)])
    submit = SubmitField('Registrar Paciente')
