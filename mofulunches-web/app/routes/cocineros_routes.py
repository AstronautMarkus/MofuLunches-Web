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

# Cocineros cartas views start

@cocineros_bp.route('/cartas-menu')
@role_required('cocineros')
def cartas_menu():
    return render_template('cocineros/cartas/cartas-menu.html', user=g.user)

@cocineros_bp.route('/cartas-list')
@role_required('cocineros')
def cartas_list():
    # Template Cards
    cartas = [
        {
            "id": 1,
            "fecha": "2024-11-16",
            "alimento": [
                {"id": 1, "nombre": "Ensalada César", "tipo": "Ensalada"},
                {"id": 2, "nombre": "Lomo Saltado", "tipo": "Almuerzo"},
                {"id": 3, "nombre": "Coca cola", "tipo": "Bebestible"}
            ],
            "calificaciones": 4.5
        },
        {
            "id": 2,
            "fecha": "2024-11-17",
            "alimento": [
                {"id": 4, "nombre": "Sopa de Pollo", "tipo": "Entrada"},
                {"id": 5, "nombre": "Pizza Margarita", "tipo": "Almuerzo"},
                {"id": 6, "nombre": "Limonada", "tipo": "Bebestible"}
            ],
            "calificaciones": 3.8
        },
        {
            "id": 3,
            "fecha": "2024-11-18",
            "alimento": [
                {"id": 7, "nombre": "Bruschetta", "tipo": "Entrada"},
                {"id": 8, "nombre": "Espagueti Carbonara", "tipo": "Almuerzo"},
                {"id": 9, "nombre": "Té Helado", "tipo": "Bebestible"}
            ],
            "calificaciones": 4.2
        },
        {
            "id": 4,
            "fecha": "2024-11-19",
            "alimento": [
                {"id": 10, "nombre": "Crema de Tomate", "tipo": "Entrada"},
                {"id": 11, "nombre": "Pollo al Curry", "tipo": "Almuerzo"},
                {"id": 12, "nombre": "Agua Mineral", "tipo": "Bebestible"}
            ],
            "calificaciones": 4.8
        },
        {
            "id": 5,
            "fecha": "2024-11-20",
            "alimento": [
                {"id": 13, "nombre": "Croquetas de Jamón", "tipo": "Entrada"},
                {"id": 14, "nombre": "Paella", "tipo": "Almuerzo"},
                {"id": 15, "nombre": "Sangría", "tipo": "Bebestible"}
            ],
            "calificaciones": 5.0
        },
        {
            "id": 6,
            "fecha": "2024-11-21",
            "alimento": [
                {"id": 16, "nombre": "Ensalada Griega", "tipo": "Ensalada"},
                {"id": 17, "nombre": "Hamburguesa Clásica", "tipo": "Almuerzo"},
                {"id": 18, "nombre": "Refresco de Naranja", "tipo": "Bebestible"}
            ],
            "calificaciones": 3.2
        },
        {
            "id": 7,
            "fecha": "2024-11-22",
            "alimento": [
                {"id": 19, "nombre": "Queso Brie con Frutas", "tipo": "Entrada"},
                {"id": 20, "nombre": "Risotto de Hongos", "tipo": "Almuerzo"},
                {"id": 21, "nombre": "Vino Blanco", "tipo": "Bebestible"}
            ],
            "calificaciones": 4.7
        },
        {
            "id": 8,
            "fecha": "2024-11-23",
            "alimento": [
                {"id": 22, "nombre": "Caprese", "tipo": "Entrada"},
                {"id": 23, "nombre": "Asado de Tira", "tipo": "Almuerzo"},
                {"id": 24, "nombre": "Cerveza Artesanal", "tipo": "Bebestible"}
            ],
            "calificaciones": 2.9
        }
    ]

    return render_template('cocineros/cartas/cartas-list.html', user=g.user, cartas=cartas)

@cocineros_bp.route('/cartas-crear')
@role_required('cocineros')
def cartas_crear():
    return render_template('cocineros/cartas/cartas-crear.html', user=g.user)

@cocineros_bp.route('/cartas-editar')
@role_required('cocineros')
def cartas_editar():
    return render_template('cocineros/cartas/cartas-editar.html', user=g.user)

@cocineros_bp.route('/cartas-eliminar')
@role_required('cocineros')
def cartas_eliminar():
    return render_template('cocineros/cartas/cartas-eliminar.html', user=g.user)

# Cocineros cartas views end

# Cocineros ingredientes views start

@cocineros_bp.route('/ingredientes-menu')
@role_required('cocineros')
def ingredientes_menu():
    return render_template('cocineros/ingredientes/ingredientes-menu.html', user=g.user)

@cocineros_bp.route('/ingredientes-list')
@role_required('cocineros')
def ingredientes_list():

    platillos = [
    {
        "id": 1,
        "nombre": "Ensalada de Lechuga y Tomate",
        "tipo": "ensalada"
    },
    {
        "id": 2,
        "nombre": "Coca cola de piña",
        "tipo": "refresco"
    },
    {
        "id": 3,
        "nombre": "Churrasco de Pescado",
        "tipo": "almuerzo"
    },
    {
        "id": 4,
        "nombre": "Churrasco Mixto",
        "tipo": "almuerzo"
    }
    ]

    return render_template('cocineros/ingredientes/ingredientes-list.html', user=g.user, platillos=platillos)

@cocineros_bp.route('/ingredientes-crear')
@role_required('cocineros')
def ingredientes_crear():
    ingredientes_categorias = [
        {"value": "", "label": "Selecciona un tipo", "selected": True},
        {"value": "almuerzo", "label": "Almuerzo"},
        {"value": "ensalada", "label": "Ensalada"},
        {"value": "refresco", "label": "Refresco"}
    ]

    return render_template(
        'cocineros/ingredientes/ingredientes-crear.html',
        user=g.user,
        ingredientes_categorias=ingredientes_categorias
    )


@cocineros_bp.route('/ingredientes-editar')
@role_required('cocineros')
def ingredientes_editar():
        
    ingredientes_categorias = [
        {"value": "", "label": "Selecciona un tipo", "selected": True},
        {"value": "almuerzo", "label": "Almuerzo"},
        {"value": "ensalada", "label": "Ensalada"},
        {"value": "refresco", "label": "Refresco"}
    ]
    
    return render_template('cocineros/ingredientes/ingredientes-editar.html', user=g.user, ingredientes_categorias=ingredientes_categorias)

@cocineros_bp.route('/ingredientes-eliminar')
@role_required('cocineros')
def ingredientes_eliminar():
    return render_template('cocineros/ingredientes/ingredientes-eliminar.html', user=g.user)

# Cocineros ingredientes views end