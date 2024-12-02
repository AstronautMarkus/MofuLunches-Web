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

        # Use a set to check for duplicates
        alimentos_unicos = set()

        for category in ['almuerzo', 'ensalada', 'refresco']:
            alimentos_ids = request.form.getlist(category + '[]')  # Get selected IDs
            print(f"Selected {category} IDs:", alimentos_ids)

            for alimento_id in alimentos_ids:
                nombre = request.form.get(f"nombre_{alimento_id}")  # Get the name
                print(f"Processing alimento: id={alimento_id}, nombre={nombre}, tipo={category}")

                if nombre:
                    # Create a unique identifier for this alimento (id and type)
                    alimento_key = (alimento_id, category)

                    if alimento_key not in alimentos_unicos:  # If not duplicated
                        alimentos_unicos.add(alimento_key)  # Add to the set
                        # Add the alimento to the list
                        alimentos.append({
                            "id": alimento_id,
                            "nombre": nombre,
                            "tipo": category
                        })
                    else:
                        print(f"Duplicated alimento ignored: id={alimento_id}, tipo={category}")

        # Validate required fields
        if not fecha or not alimentos:
            flash('Debes completar todos los campos y seleccionar al menos un alimento.', 'danger')
            return redirect(url_for('cocineros.cartas_crear'))

        # Payload for the API
        data = {
            "fecha": fecha,
            "alimentos": alimentos
        }

        # Send POST request to the API
        response = requests.post(f"{API_URL}/cartas", json=data)

        if response.status_code == 201:
            api_message = response.json().get('message', 'Carta created successfully.')
            flash(api_message, 'success')
            return redirect(url_for('cocineros.cartas_list'))
        else:
            # Extract error message from the API response
            api_message = response.json().get('message', 'Error creating the carta.')
            print("Error in POST:", response.status_code, response.text)
            flash(api_message, 'danger')

    # If it is a GET request
    response = requests.get(f"{API_URL}/alimentos")
    if response.status_code == 200:
        alimentos = response.json()
    else:
        return render_template(
            'cocineros/cartas/cartas-crear.html',
            user=g.user,
            service_offline=True
        )

    # Classify alimentos by type
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
    service_offline = response.status_code != 200
    ingredientes = response.json() if not service_offline else []
    return render_template(
        'cocineros/ingredientes/ingredientes-list.html',
        user=g.user,
        ingredientes=ingredientes,
        service_offline=service_offline
    )

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
    
    response = requests.get(f"{API_URL}/alimentos")
    service_offline = response.status_code != 200
    ingredientes_categorias = [
        {"value": "", "label": "Selecciona un tipo", "selected": True},
        {"value": "almuerzo", "label": "Almuerzo"},
        {"value": "ensalada", "label": "Ensalada"},
        {"value": "refresco", "label": "Refresco"}
    ]
    return render_template(
        'cocineros/ingredientes/ingredientes-crear.html',
        user=g.user,
        ingredientes_categorias=ingredientes_categorias,
        service_offline=service_offline
    )

@cocineros_bp.route('/ingredientes-editar/<int:ingrediente_id>', methods=['GET', 'POST'])
@role_required('cocineros')
def ingredientes_editar(ingrediente_id):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        data = {
            "nombre": nombre,
            "tipo": tipo
        }
        response = requests.put(f"{API_URL}/alimentos/{ingrediente_id}", json=data)
        if response.status_code == 200:
            flash('Ingrediente actualizado exitosamente', 'success')
            return redirect(url_for('cocineros.ingredientes_menu'))
        else:
            flash('Error al actualizar el ingrediente', 'danger')
    
    response = requests.get(f"{API_URL}/alimentos/{ingrediente_id}")
    service_offline = response.status_code != 200
    if service_offline:
        return render_template(
            'cocineros/ingredientes/ingredientes-editar.html',
            user=g.user,
            service_offline=service_offline
        )
    
    ingrediente = response.json()
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
        ingredientes_categorias=ingredientes_categorias,
        service_offline=service_offline
    )

@cocineros_bp.route('/ingredientes-eliminar')
@role_required('cocineros')
def ingredientes_eliminar():
    return render_template('cocineros/ingredientes/ingredientes-eliminar.html', user=g.user)

# Cocineros ingredientes views end


# Cocineros pedidos views start

@cocineros_bp.route('/pedidos-menu')
@role_required('cocineros')
def pedidos_menu():
    return render_template('cocineros/pedidos/pedidos-menu.html', user=g.user)

@cocineros_bp.route('/pedidos-list')
@role_required('cocineros')
def pedidos_list():
    response = requests.get(f"{API_URL}/pedidos")
    if response.status_code == 200:
        pedidos = response.json()
    else:
        pedidos = []
        flash('Error al obtener la lista de pedidos.', 'danger')
    
    return render_template('cocineros/pedidos/pedidos-list.html', user=g.user, pedidos=pedidos)

@cocineros_bp.route('/pedidos-diarios')
@role_required('cocineros')
def pedidos_diarios():
    response = requests.get(f"{API_URL}/pedidos/diarios")
    if response.status_code == 200:
        pedidos = response.json()
    else:
        pedidos = []
        flash('Error al obtener la lista de pedidos diarios.', 'danger')
    
    return render_template('cocineros/pedidos/pedidos-list.html', user=g.user, pedidos=pedidos)

@cocineros_bp.route('/pedidos-por-rut/<rut>')
@role_required('cocineros')
def pedidos_por_rut(rut):
    response = requests.get(f"{API_URL}/pedidos/{rut}")
    if response.status_code == 200:
        pedidos = response.json()
    else:
        pedidos = []
        flash(f'Error al obtener la lista de pedidos para el RUT {rut}.', 'danger')
    
    return render_template('cocineros/pedidos/pedidos-list.html', user=g.user, pedidos=pedidos)

@cocineros_bp.route('/pedidos-diarios-por-rut/<rut>')
@role_required('cocineros')
def pedidos_diarios_por_rut(rut):
    response = requests.get(f"{API_URL}/pedidos/diarios/{rut}")
    if response.status_code == 200:
        pedidos = response.json()
    else:
        pedidos = []
        flash(f'Error al obtener el pedido diario para el RUT {rut}.', 'danger')
    
    return render_template('cocineros/pedidos/pedidos-list.html', user=g.user, pedidos=pedidos)

@cocineros_bp.route('/pedidos-actualizar/<cod_unico>', methods=['POST'])
@role_required('cocineros')
def pedidos_actualizar(cod_unico):
    nuevo_estado = request.form.get('estado')
    nueva_hora_retiro = request.form.get('hora_retiro')
    
    if not nuevo_estado and not nueva_hora_retiro:
        flash('Debe proporcionar un nuevo estado o una nueva hora de retiro.', 'danger')
        return redirect(url_for('cocineros.pedidos_list'))

    data = {}
    if nuevo_estado:
        data['estado'] = nuevo_estado
    if nueva_hora_retiro:
        data['hora_retiro'] = nueva_hora_retiro

    response = requests.put(f"{API_URL}/pedidos/{cod_unico}", json=data)
    if response.status_code == 200:
        flash('Pedido actualizado exitosamente.', 'success')
    else:
        error_message = response.json().get('message', 'Error al actualizar el pedido.')
        flash(error_message, 'danger')

    return redirect(url_for('cocineros.pedidos_list'))

# Cocineros pedidos views end