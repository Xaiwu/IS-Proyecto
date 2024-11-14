from DataBase.DataBase import insertar_paciente, obtener_datos_citas
from .forms import AsistenteReservaForm, PacienteForm
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
import sqlite3
from .forms import RegistroForm, ReservaForm, AsistenteReservaForm, PacienteForm
from DataBase.DataBase import (insertar_especialista, insertar_paciente, insertar_cita,
                               obtener_datos_especialistas, obtener_datos_pacientes, obtener_datos_citas, citas_especialista)

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/servicios')
def servicios():
    return render_template('servicios.html')


@bp.route('/reservar')
def reservar():
    form = ReservaForm()
    especialistas = obtener_datos_especialistas()
    if especialistas:
        form.especialista.choices = [(e[0], e[1]) for e in especialistas]
    else:
        form.especialista.choices = []
    return render_template('reservar.html', form=form, especialistas=especialistas)


@bp.route('/reserva', methods=['GET', 'POST'])
def reserva():
    form = ReservaForm()
    especialistas = obtener_datos_especialistas()
    if especialistas:
        form.especialista.choices = [(e[0], e[1]) for e in especialistas]
    else:
        form.especialista.choices = []

    # Inicializa las opciones de hora
    todas_horas = ["09:00", "10:00", "11:00", "12:00",
                   "13:00", "14:00", "15:00", "16:00", "17:00"]
    form.hora.choices = [(hora, hora) for hora in todas_horas]

    if form.validate_on_submit():
        fecha = form.fecha.data
        hora = form.hora.data
        id_especialista = form.especialista.data
        id_paciente = 1  # Aquí deberías obtener el id del paciente autenticado
        if insertar_cita(fecha, hora, id_especialista, id_paciente):
            flash('Cita reservada con éxito')
        else:
            flash('El especialista no está disponible en esa fecha y hora')
        return redirect(url_for('main.reserva'))
    return render_template('reservar.html', form=form, especialistas=especialistas)


@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        insertar_paciente(form.nombre.data,
                          form.telefono.data, form.direccion.data)
        flash('Registro exitoso')
        return redirect(url_for('main.index'))
    return render_template('registro.html', form=form)


@bp.route('/ver_datos')
def ver_datos():
    especialistas = obtener_datos_especialistas()
    pacientes = obtener_datos_pacientes()
    citas = obtener_datos_citas()
    return render_template('ver_datos.html', especialistas=especialistas, pacientes=pacientes, citas=citas)


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


@bp.route('/asistente/insertar_paciente', methods=['GET', 'POST'])
def insertar_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        telefono = form.telefono.data
        direccion = form.direccion.data
        insertar_paciente(nombre, telefono, direccion)
        flash('Paciente insertado con éxito')
        return redirect(url_for('main.asistente_ver_citas'))
    return render_template('insertar_paciente.html', form=form)


@bp.route('/asistente/reservar', methods=['GET', 'POST'])
def asistente_reservar():
    form = AsistenteReservaForm()
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
        id_paciente = form.paciente.data
        id_asistente = 1  # Aquí deberías obtener el id del asistente autenticado
        if insertar_cita(fecha, hora, id_especialista, id_paciente, id_asistente):
            flash('Cita reservada/modificada con éxito')
        else:
            flash('El especialista no está disponible en esa fecha y hora')
    return render_template('asistente_reservar.html', form=form, pacientes=pacientes)


@bp.route('/asistente/cancelar_cita/<int:cita_id>', methods=['POST'])
def cancelar_cita(cita_id):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM Citas WHERE id = ?", (cita_id,))
    con.commit()
    con.close()
    flash('Cita cancelada con éxito')
    return redirect(url_for('main.asistente_ver_citas'))


@bp.route('/asistente/ver_citas', methods=['GET', 'POST'])
def asistente_ver_citas():
    form = PacienteForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        telefono = form.telefono.data
        direccion = form.direccion.data
        insertar_paciente(nombre, telefono, direccion)
        flash('Paciente insertado con éxito')
        return redirect(url_for('main.asistente_ver_citas'))

    citas = obtener_datos_citas()
    return render_template('asistente_ver_citas.html', citas=citas, form=form)
