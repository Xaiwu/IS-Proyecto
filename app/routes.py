from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
import sqlite3
from DataBase.DataBase import insertar_paciente, citas_pacientes, obtener_datos_citas, actualizar_cita, obtener_cita, obtener_datos_pacientes, citas_especialista, insertar_cita, obtener_datos_especialistas
from .forms import AsistenteReservaForm, PacienteForm, ReservaForm

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
    cita = obtener_cita(cita_id)
    if cita:
        form.fecha.data = cita[1]
        form.hora.data = cita[2]
        form.especialista.data = cita[3]
        form.paciente.data = cita[4]

    if form.validate_on_submit():
        actualizar_cita(cita_id, form.fecha.data, form.hora.data,
                        form.especialista.data, form.paciente.data)
        flash('Cita modificada con éxito')
        return redirect(url_for('main.asistente'))

    especialistas = obtener_datos_especialistas()
    pacientes = obtener_datos_pacientes()
    form.especialista.choices = [(e[0], e[1]) for e in especialistas]
    form.paciente.choices = [(p[0], p[1]) for p in pacientes]

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
