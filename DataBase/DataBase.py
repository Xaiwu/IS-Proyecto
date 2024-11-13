import sqlite3

def crear_database():
    db = open("centro_medico.db", "x")
    db.close()

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
        CREATE TABLE IF NOT EXISTS Citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            id_especialista INTEGER,
            id_paciente INTEGER,
            FOREIGN KEY (id_especialista) REFERENCES Especialistas(id),
            FOREIGN KEY (id_paciente) REFERENCES Pacientes(id)
    )      
    """)

    con.commit()
    con.close()

def insertar_especialista(nombre:str, especialidad:str):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO Especialistas (nombre, especialidad) VALUES (?, ?)", (nombre, especialidad))
    con.commit()
    con.close()

def insertar_paciente(nombre:str, telefono:str, direccion:str):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO Pacientes (nombre, telefono, direccion) VALUES (?, ?, ?)", (nombre, telefono, direccion))
    con.commit()
    con.close()

def insertar_cita(fecha: str, hora: str, id_especialista:int, id_paciente:int):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO Citas (fecha, hora, id_especialista, id_paciente) VALUES (?, ?, ?, ?)", (fecha, hora, id_especialista, id_paciente))
    con.commit()
    con.close()

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

def citas_especialista(id_especialista):
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM Citas WHERE id_especialista = {id_especialista}")
    datos = cursor.fetchall()
    con.close()
    return datos