from flask import render_template
from app import create_app

app = create_app()

# Se definiran las rutas de la aplicacion y la logica asociada a cada ruta (clase)


@app.route('/')
def index():
    return render_template('index.html')
