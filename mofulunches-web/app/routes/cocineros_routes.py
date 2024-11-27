from flask import Blueprint, render_template, session, g, request, redirect, url_for, flash
from functools import wraps
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv('API_URL')

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
    return render_template('cocineros/index.html', user=g.user)

# Cocineros cartas views start

@cocineros_bp.route('/cartas-menu')
@role_required('cocineros')
def cartas_menu():
    return render_template('cocineros/cartas/cartas-menu.html', user=g.user)

@cocineros_bp.route('/cartas-list')
@role_required('cocineros')
def cartas_list():
    # Get filter parameters
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    
    # Prepare query parameters
    params = {}
    if desde:
        params['desde'] = desde
    if hasta:
        params['hasta'] = hasta

    # Fetch filtered cards
    response = requests.get(f"{API_URL}/cartas", params=params)
    if response.status_code == 200:
        cartas = response.json()
    else:
        cartas = []
    
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

    response = requests.get(f"{API_URL}/alimentos")
    if response.status_code == 200:
        ingredientes = response.json()
    else:
        ingredientes = []

    return render_template('cocineros/ingredientes/ingredientes-list.html', user=g.user, ingredientes=ingredientes)

@cocineros_bp.route('/ingredientes-crear', methods=['GET', 'POST'])
@role_required('cocineros')
def ingredientes_crear():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        
        data = {
            "nombre": nombre,
            "tipo": tipo
        }
        
        response = requests.post(f"{API_URL}/alimentos", json=data)
        
        if response.status_code == 201:
            flash('Ingrediente creado exitosamente', 'success')
            return redirect(url_for('cocineros.ingredientes_menu'))
        else:
            flash('Error al crear el ingrediente', 'danger')
    
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