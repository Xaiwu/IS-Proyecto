from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
import sqlite3
from DataBase.DataBase import insertar_paciente, citas_pacientes, obtener_datos_citas, actualizar_cita, obtener_cita, obtener_datos_pacientes, citas_especialista, insertar_cita, obtener_datos_especialistas, obtener_citas_semana
from .forms import AsistenteReservaForm, PacienteForm, ReservaForm
from datetime import datetime, timedelta
import calendar

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/servicios')
def servicios():
    return render_template('servicios.html')


# @bp.route('/reserva')
# def reserva():

#     return render_template('reservar.html')


@bp.route('/reservar', methods=['GET', 'POST'])
def reservar():
    form = ReservaForm()
    especialistas = obtener_datos_especialistas()
    pacientes = obtener_datos_pacientes()

    if especialistas:
        form.especialista.choices = [(e[0], e[1]) for e in especialistas]
    else:
        form.especialista.choices = []

    if pacientes:
        form.paciente.choices = [(p[0], p[1]) for p in pacientes]
    else:
        form.paciente.choices = []

    todas_horas = ["09:00", "10:00", "11:00", "12:00",
                   "13:00", "14:00", "15:00", "16:00", "17:00"]
    form.hora.choices = [(hora, hora) for hora in todas_horas]

    if form.validate_on_submit():
        fecha = form.fecha.data
        hora = form.hora.data
        id_especialista = form.especialista.data
        id_paciente = 1  # Obtener el id del paciente seleccionado
        if insertar_cita(fecha, hora, id_especialista, id_paciente):
            flash('Cita reservada con éxito')
        else:
            flash('El especialista no está disponible en esa fecha y hora')
        return redirect(url_for('main.reservar'))

    return render_template('reservar.html', form=form)


@bp.route('/ver_datos')
def ver_datos():
    especialistas = obtener_datos_especialistas()
    pacientes = obtener_datos_pacientes()
    citas = obtener_datos_citas()
    return render_template('ver_datos.html', especialistas=especialistas, pacientes=pacientes, citas=citas)


@bp.route('/asistente', methods=['GET', 'POST'])
def asistente():
    form_paciente = PacienteForm()
    form_reserva = AsistenteReservaForm()
    pacientes = obtener_datos_pacientes()
    citas = []

    # Poblar las opciones del formulario antes de la validación
    especialistas = obtener_datos_especialistas()
    todas_horas = ["09:00", "10:00", "11:00", "12:00",
                   "13:00", "14:00", "15:00", "16:00", "17:00"]

    form_reserva.especialista.choices = [(e[0], e[1]) for e in especialistas]
    form_reserva.paciente.choices = [(p[0], p[1]) for p in pacientes]
    form_reserva.hora.choices = [(hora, hora) for hora in todas_horas]

    if request.method == 'POST':
        if 'nombre' in request.form:
            # Registro de paciente
            if form_paciente.validate_on_submit():
                nombre = form_paciente.nombre.data
                telefono = form_paciente.telefono.data
                direccion = form_paciente.direccion.data
                insertar_paciente(nombre, telefono, direccion)
                flash('Paciente insertado con éxito')
                return redirect(url_for('main.asistente'))
        elif 'fecha' in request.form:
            # Asignar nueva cita
            if form_reserva.validate_on_submit():
                fecha = form_reserva.fecha.data
                hora = form_reserva.hora.data
                id_especialista = form_reserva.especialista.data
                id_paciente = form_reserva.paciente.data
                id_asistente = 1  # Aquí deberías obtener el id del asistente autenticado
                if insertar_cita(fecha, hora, id_especialista, id_paciente, id_asistente):
                    flash('Cita reservada/modificada con éxito')
                else:
                    flash('El especialista no está disponible en esa fecha y hora')
                return redirect(url_for('main.asistente'))

    if request.method == 'GET' and 'paciente_id' in request.args:
        paciente_id = request.args.get('paciente_id')
        if paciente_id:
            citas = citas_pacientes(paciente_id)

    return render_template('asistente.html', form_paciente=form_paciente, form_reserva=form_reserva, pacientes=pacientes, citas=citas)


@bp.route('/asistente/modificar_cita/<int:cita_id>', methods=['GET', 'POST'])
def modificar_cita(cita_id):
    form = AsistenteReservaForm()

    # Poblar las opciones del formulario antes de la validación
    especialistas = obtener_datos_especialistas()
    pacientes = obtener_datos_pacientes()
    todas_horas = ["09:00", "10:00", "11:00", "12:00",
                   "13:00", "14:00", "15:00", "16:00", "17:00"]

    form.especialista.choices = [(e[0], e[1]) for e in especialistas]
    form.paciente.choices = [(p[0], p[1]) for p in pacientes]
    form.hora.choices = [(hora, hora) for hora in todas_horas]

    cita = obtener_cita(cita_id)
    if cita and request.method == 'GET':
        # Convierte la fecha a un objeto datetime
        form.fecha.data = datetime.strptime(cita[1], '%Y-%m-%d')
        form.hora.data = cita[2]
        form.especialista.data = cita[3]
        form.paciente.data = cita[4]

    if request.method == 'POST':
        print("Formulario enviado con método POST")
        if form.validate_on_submit():
            print("Formulario validado correctamente")
            actualizar_cita(cita_id, form.fecha.data, form.hora.data,
                            form.especialista.data, form.paciente.data)
            flash('Cita modificada con éxito')
            return redirect(url_for('main.asistente'))
        else:
            print("Errores de validación del formulario:", form.errors)

    return render_template('asistente_reservar.html', form=form)


@bp.route('/asistente/cancelar_cita/<int:cita_id>', methods=['POST'])
def cancelar_cita(cita_id):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM Citas WHERE id = ?", (cita_id,))
    con.commit()
    con.close()
    flash('Cita cancelada con éxito')
    return redirect(url_for('main.asistente'))


@bp.route('/obtener_horas_disponibles', methods=['GET'])
def obtener_horas_disponibles():
    fecha = request.args.get('fecha')
    id_especialista = request.args.get('especialista_id')
    citas = citas_especialista(id_especialista)
    horas_ocupadas = [cita[2] for cita in citas]
    todas_horas = ["09:00", "10:00", "11:00", "12:00",
                   "13:00", "14:00", "15:00", "16:00", "17:00"]
    horas_disponibles = [
        hora for hora in todas_horas if hora not in horas_ocupadas]
    return jsonify(horas=horas_disponibles)

@bp.route('/obtener_citas_paciente', methods=['GET'])
def obtener_citas_paciente():
    id_paciente = request.args.get('paciente_id')
    citas = citas_pacientes(id_paciente)
    return jsonify(citas=citas)


@bp.route('/ver_citas', methods=['GET'])
def ver_citas():
    medico_id = request.args.get('medico')
    citas = citas_especialista(medico_id)
    return render_template('ver_citas.html', citas=citas)

@bp.route('/calendario', methods=['GET'])
def calendario():
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    medico_id = request.args.get('medico', type=int)
    print("Medico ID:", medico_id)  # Agrega esta línea para depurar
    if medico_id is None:
        flash('Debe seleccionar un médico.')
        return redirect(url_for('main.medico'))
    citas = citas_especialista(medico_id)
    return render_template('calendario.html', year=year, month=month, citas=citas, calendar=calendar, timedelta=timedelta)

@bp.route('/semana', methods=['GET'])
def semana():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)
    start_date = datetime(year, month, day) - timedelta(days=datetime(year, month, day).weekday())
    end_date = start_date + timedelta(days=6)
    citas = obtener_citas_semana(start_date, end_date)
    print("Citas obtenidas:", citas)  # Agrega esta línea para depurar
    return render_template('semana.html', start_date=start_date, end_date=end_date, citas=citas, timedelta=timedelta)

@bp.route('/medico', methods=['GET'])
def medico():
    especialistas = obtener_datos_especialistas()
    return render_template('seleccionar_medico.html', especialistas=especialistas)