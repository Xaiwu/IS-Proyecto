import sqlite3


def vaciar_especialistas():
    con = sqlite3.connect("centro_medico.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM Especialistas")
    con.commit()
    con.close()


vaciar_especialistas()
print("Tabla de especialistas vaciada correctamente.")
