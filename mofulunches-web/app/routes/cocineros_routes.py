from flask import Blueprint, render_template, session, g
from functools import wraps

cocineros_bp = Blueprint('cocineros', __name__, url_prefix='/cocineros')

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user or g.user.get("role") != role:
                error_message = "Acceso denegado. Debes ser cocinero para acceder a esta página."
                return render_template('error.html', error_message=error_message)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@cocineros_bp.before_request
def before_request():
    g.user = session.get('user')

@cocineros_bp.route('/')
@role_required('cocineros')
def cocineros_index():
    return render_template('cocineros/cocineros-menu.html', user=g.user)

@cocineros_bp.route('/cartas-menu')
@role_required('cocineros')
def cartas_menu():
    return render_template('cocineros/cartas-menu.html', user=g.user)

@cocineros_bp.route('/cartas-list')
@role_required('cocineros')
def cartas_list():
    # Template Cards
    cartas = [
        {
            "id": 1,
            "fecha": "2024-11-16",
            "alimento": [
                {"id": 1, "nombre": "Ensalada César", "tipo": "Entrada"},
                {"id": 2, "nombre": "Lomo Saltado", "tipo": "Plato Fuerte"},
                {"id": 3, "nombre": "Tarta de Limón", "tipo": "Postre"}
            ],
            "calificaciones": 4.5
        },
        {
            "id": 2,
            "fecha": "2024-11-17",
            "alimento": [
                {"id": 4, "nombre": "Sopa de Tomate", "tipo": "Entrada"},
                {"id": 5, "nombre": "Pollo a la Parrilla", "tipo": "Plato Fuerte"},
                {"id": 6, "nombre": "Helado de Vainilla", "tipo": "Postre"}
            ],
            "calificaciones": 2.1
        },
        {
            "id": 3,
            "fecha": "2024-11-18",
            "alimento": [
                {"id": 7, "nombre": "Bruschetta", "tipo": "Entrada"},
                {"id": 8, "nombre": "Risotto de Champiñones", "tipo": "Plato Fuerte"},
                {"id": 9, "nombre": "Brownie con Helado", "tipo": "Postre"},
            ],
            "calificaciones": 1.5
        }
    ]
    return render_template('cocineros/cartas-list.html', user=g.user, cartas=cartas)

@cocineros_bp.route('/cartas-crear')
@role_required('cocineros')
def cartas_crear():
    return render_template('cocineros/cartas-crear.html', user=g.user)


@cocineros_bp.route('/platillos-menu')
@role_required('cocineros')
def platillos_menu():
    return render_template('cocineros/platillos-menu.html', user=g.user)

@cocineros_bp.route('/ingredientes-menu')
@role_required('cocineros')
def ingredientes_menu():
    return render_template('cocineros/ingredientes-menu.html', user=g.user)


