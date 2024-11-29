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

    # Fetch all cards (for `hay_cartas` check)
    response_all = requests.get(f"{API_URL}/cartas")
    if response_all.status_code != 200:
        return render_template(
            'cocineros/cartas/cartas-list.html',
            user=g.user,
            service_offline=True
        )
    hay_cartas = len(response_all.json()) > 0

    # Fetch filtered cards
    response = requests.get(f"{API_URL}/cartas", params=params)
    if response.status_code == 200:
        cartas = response.json()
    else:
        cartas = []
    
    return render_template(
        'cocineros/cartas/cartas-list.html',
        user=g.user,
        cartas=cartas,
        hay_cartas=hay_cartas,
        service_offline=False
    )


@cocineros_bp.route('/cartas-crear', methods=['GET', 'POST'])
@role_required('cocineros')
def cartas_crear():
    if request.method == 'POST':
        
        fecha = request.form.get('fecha')

        alimentos = []

        for category in ['almuerzo', 'ensalada', 'refresco']:
            alimentos_ids = request.form.getlist(category + '[]')  
            print(f"IDs de {category} seleccionados:", alimentos_ids) 

            for alimento_id in alimentos_ids:
                nombre = request.form.get(f"nombre_{alimento_id}")
                print(f"Procesando alimento: id={alimento_id}, nombre={nombre}")  
                if nombre:  
                    alimentos.append({"id": alimento_id, "nombre": nombre})


        if not fecha or not alimentos:
            flash('Debes completar todos los campos y seleccionar al menos un alimento.', 'danger')
            return redirect(url_for('cocineros.cartas_crear'))
        
        
        data = {
            "fecha": fecha,
            "alimentos": alimentos
        }
       
        response = requests.post(f"{API_URL}/cartas", json=data)
        
        if response.status_code == 201:
            flash('Carta creada exitosamente.', 'success')
            return redirect(url_for('cocineros.cartas_list'))
        else:
            print("Error en el POST:", response.status_code, response.text) 
            flash('Error al crear la carta.', 'danger')

    
    response = requests.get(f"{API_URL}/alimentos")
    if response.status_code == 200:
        alimentos = response.json()
    else:
        return render_template(
            'cocineros/cartas/cartas-crear.html',
            user=g.user,
            service_offline=True
        )
    
    alimentos_categorias = {
        "almuerzo": [alimento for alimento in alimentos if alimento["tipo"] == "almuerzo"],
        "ensalada": [alimento for alimento in alimentos if alimento["tipo"] == "ensalada"],
        "refresco": [alimento for alimento in alimentos if alimento["tipo"] == "refresco"]
    }
    
    return render_template(
        'cocineros/cartas/cartas-crear.html',
        user=g.user,
        alimentos_categorias=alimentos_categorias,
        service_offline=False
    )


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


@cocineros_bp.route('/ingredientes-editar/<int:ingrediente_id>', methods=['GET', 'POST'])
@role_required('cocineros')
def ingredientes_editar(ingrediente_id):
    if request.method == 'POST':
        # Get user input
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        
        # Create payload
        data = {
            "nombre": nombre,
            "tipo": tipo
        }
        
        # Send request to API
        response = requests.put(f"{API_URL}/alimentos/{ingrediente_id}", json=data)
        
        if response.status_code == 200:
            flash('Ingrediente actualizado exitosamente', 'success')
            return redirect(url_for('cocineros.ingredientes_menu'))
        else:
            flash('Error al actualizar el ingrediente', 'danger')
    
    # Get ingredient data
    response = requests.get(f"{API_URL}/alimentos/{ingrediente_id}")
    
    if response.status_code != 200:
        flash('Error al obtener los datos del ingrediente', 'danger')
        return redirect(url_for('cocineros.ingredientes_menu'))
    
    ingrediente = response.json()
    
    # Alimento categories
    ingredientes_categorias = [
        {"value": "", "label": "Selecciona un tipo", "selected": not ingrediente.get('tipo')},
        {"value": "almuerzo", "label": "Almuerzo", "selected": ingrediente.get('tipo') == "almuerzo"},
        {"value": "ensalada", "label": "Ensalada", "selected": ingrediente.get('tipo') == "ensalada"},
        {"value": "refresco", "label": "Refresco", "selected": ingrediente.get('tipo') == "refresco"}
    ]
    
    return render_template(
        'cocineros/ingredientes/ingredientes-editar.html',
        user=g.user,
        ingrediente=ingrediente,
        ingredientes_categorias=ingredientes_categorias
    )


@cocineros_bp.route('/ingredientes-eliminar')
@role_required('cocineros')
def ingredientes_eliminar():
    return render_template('cocineros/ingredientes/ingredientes-eliminar.html', user=g.user)

# Cocineros ingredientes views end