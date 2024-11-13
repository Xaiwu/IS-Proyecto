from flask import render_template, Blueprint

bp = Blueprint('main', __name__)

# Se definiran las rutas de la aplicacion y la logica asociada a cada ruta (clase)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/reservar')
def reservar():
    return render_template('reservar.html') 