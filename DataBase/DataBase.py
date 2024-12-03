import sqlite3
from datetime import datetime

def crear_database():
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Especialistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Asistentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            id_especialista INTEGER,
            id_paciente INTEGER,
            id_asistente INTEGER,
            FOREIGN KEY (id_especialista) REFERENCES Especialistas(id),
            FOREIGN KEY (id_paciente) REFERENCES Pacientes(id),
            FOREIGN KEY (id_asistente) REFERENCES Asistentes(id)
    )      
    """)

    con.commit()
    con.close()


def insertar_especialista(nombre, especialidad):
    conn = sqlite3.connect('centro_medico.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Especialistas (nombre, especialidad)
        VALUES (?, ?)
    ''', (nombre, especialidad))
    conn.commit()
    conn.close()


def insertar_paciente(nombre: str, telefono: str, direccion: str):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO Pacientes (nombre, telefono, direccion) VALUES (?, ?, ?)",
                   (nombre, telefono, direccion))
    con.commit()
    con.close()


def insertar_cita(fecha: str, hora: str, id_especialista: int, id_paciente: int):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()

    # Verificar disponibilidad del especialista
    cursor.execute("SELECT * FROM Citas WHERE fecha = ? AND hora = ? AND id_especialista = ?",
                   (fecha, hora, id_especialista))
    cita_existente = cursor.fetchone()

    if cita_existente:
        con.close()
        return False  # El especialista no está disponible en la fecha y hora solicitadas

    cursor.execute("INSERT INTO Citas (fecha, hora, id_especialista, id_paciente) VALUES (?, ?, ?, ?)",
                   (fecha, hora, id_especialista, id_paciente))
    con.commit()
    con.close()
    return True  # La cita se reservó con éxito


def obtener_datos_especialistas():
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Especialistas")
    datos = cursor.fetchall()
    con.close()
    return datos


def obtener_datos_pacientes():
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Pacientes")
    datos = cursor.fetchall()
    con.close()
    return datos

def obtener_datos_paciente(paciente_id):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Pacientes WHERE id = ?", (paciente_id,))
    datos = cursor.fetchone()
    con.close()
    return datos


def obtener_datos_citas():
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Citas")
    datos = cursor.fetchall()
    con.close()
    return datos


def citas_pacientes(id_paciente):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM Citas WHERE id_paciente = {id_paciente}")
    datos = cursor.fetchall()
    con.close()
    return datos


def citas_especialista(medico_id):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Citas.fecha, Citas.hora, Pacientes.nombre, Especialistas.nombre
        FROM Citas
        JOIN Pacientes ON Citas.id_paciente = Pacientes.id
        JOIN Especialistas ON Citas.id_especialista = Especialistas.id
        WHERE Citas.id_especialista = ?
    """, (medico_id,))
    datos = cursor.fetchall()
    con.close()
    return datos


def actualizar_cita(cita_id, fecha, hora, id_especialista, id_paciente):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("""
        UPDATE Citas
        SET fecha = ?, hora = ?, id_especialista = ?, id_paciente = ?
        WHERE id = ?
    """, (fecha, hora, id_especialista, id_paciente, cita_id))
    con.commit()
    con.close()


def obtener_cita(cita_id):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Citas WHERE id = ?", (cita_id,))
    datos = cursor.fetchone()
    con.close()
    return datos


def citas_pacientes(id_paciente):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Citas.id, Citas.fecha, Citas.hora, Especialistas.nombre
        FROM Citas
        JOIN Especialistas ON Citas.id_especialista = Especialistas.id
        WHERE Citas.id_paciente = ?
    """, (id_paciente,))
    datos = cursor.fetchall()
    con.close()
    return datos

def obtener_citas_semana(start_date, end_date):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Citas.fecha, Citas.hora, Pacientes.nombre, Especialistas.nombre
        FROM Citas
        JOIN Pacientes ON Citas.id_paciente = Pacientes.id
        JOIN Especialistas ON Citas.id_especialista = Especialistas.id
        WHERE fecha BETWEEN ? AND ?
    """, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    datos = cursor.fetchall()
    con.close()
    return datos

def eliminar_cita(cita_id):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM Citas WHERE id = ?", (cita_id))
    con.commit()
    con.close()
