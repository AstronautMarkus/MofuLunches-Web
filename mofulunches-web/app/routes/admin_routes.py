from flask import Blueprint, render_template, session, g, request, flash, redirect, url_for
from functools import wraps
from dotenv import load_dotenv
import requests
import os



load_dotenv()
API_URL = os.getenv('API_URL')

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user or g.user.get("role") != role:
                error_message = "Acceso denegado. Debes ser administrador para acceder a esta página."
                return render_template('error.html', error_message=error_message)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@admin_bp.before_request
def before_request():
    g.user = session.get('user')

@admin_bp.route('/')
@role_required('admin')
def admin_index():
    return render_template('admin/index.html', user=g.user)

@admin_bp.route('/usuarios-list')
@role_required('admin')
def admin_usuarios():
    try:
        response = requests.get(f"{API_URL}/usuarios")
        if response.status_code == 200:
            usuarios = response.json()
            service_offline = False
        else:
            usuarios = []
            service_offline = True
    except requests.RequestException:
        usuarios = []
        service_offline = True

    return render_template('admin/admin_listar_usuarios.html', user=g.user, usuarios=usuarios, service_offline=service_offline)

@admin_bp.route('/crear-usuario', methods=['GET', 'POST'])
@role_required('admin')
def crear_usuario():
    usuario_roles = [
        {"valor": "admin", "nombre": "Administrador"},
        {"valor": "empleado", "nombre": "Empleado"},
        {"valor": "cocineros", "nombre": "Cocineros"}
    ]

    service_offline = False

    # Ping the user list API to check if the service is online
    try:
        response = requests.get(f"{API_URL}/usuarios")
        if response.status_code != 200:
            service_offline = True
    except requests.RequestException:
        service_offline = True

    if request.method == 'POST' and not service_offline:
        # User data
        nombre = request.form.get('nombre').capitalize()
        apellido = request.form.get('apellido').capitalize()
        correo = request.form.get('correo').lower()
        contrasena = request.form.get('contrasena')
        rut = request.form.get('rut')
        codigo_RFID = request.form.get('codigo_RFID')
        tipo_usuario = request.form.get('tipo_usuario').lower()

        # Clean dot and dash from rut
        if rut:
            rut = rut.replace('.', '').replace('-', '')

        # Form data
        data = {
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'contrasena': contrasena,
            'rut': rut,
            'tipo_usuario': tipo_usuario
        }

        if codigo_RFID:
            data['codigo_RFID'] = codigo_RFID

        try:
            response = requests.post(f"{API_URL}/usuarios", json=data)
            response_data = response.json()  # Convert to json

            if response.status_code == 201:
                # If user created successfully
                message = response_data.get('message', 'Usuario creado exitosamente.')
                flash(message, 'success')
                return redirect(url_for('admin.admin_usuarios'))
            else:
                # If message are not 201
                error_message = response_data.get('error', 'Error al crear el usuario.')
                flash(error_message, 'danger')

        except ValueError:
            # If no json data is returned
            flash('No se pudo procesar la respuesta del servidor.', 'danger')
        except requests.RequestException as e:
            # Error handling API request
            flash(f'Error al conectar con la API: {e}', 'danger')
            service_offline = True

    return render_template('admin/admin_crear_usuario.html', user=g.user, roles=usuario_roles, service_offline=service_offline)


@admin_bp.route('/editar-usuario/<rut>', methods=['GET', 'POST'])
@role_required('admin')
def editar_usuario(rut):
    usuario_roles = [
        {"valor": "admin", "nombre": "Administrador"},
        {"valor": "empleado", "nombre": "Empleado"},
        {"valor": "cocineros", "nombre": "Cocineros"}
    ]

    service_offline = False

    try:
        # Get API Data
        response = requests.get(f"{API_URL}/usuarios/{rut}")
        if response.status_code == 200:
            usuario = response.json()
        else:
            flash('No se pudo obtener la información del usuario.', 'danger')
            return redirect(url_for('admin.admin_usuarios'))
    except requests.RequestException as e:
        flash(f'Error al conectar con la API: {e}', 'danger')
        return redirect(url_for('admin.admin_usuarios'))

    if request.method == 'POST':
        # Get form data
        nombre = request.form.get('nombre').capitalize()
        apellido = request.form.get('apellido').capitalize()
        correo = request.form.get('correo').lower()
        codigo_RFID = request.form.get('codigo_RFID')
        tipo_usuario = request.form.get('tipo_usuario').lower()


        # Check if user is trying to change its role to admin
        if g.user['rut'] == rut and tipo_usuario != "admin":
            flash('¡No puedes cambiarte el rol de administrador!', 'danger')
            return render_template(
                'admin/admin_editar_usuario.html',
                user=g.user,
                usuario=usuario,  # user dict
                roles=usuario_roles,
                show_modal=True
            )

        # Data for API
        data = {
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'tipo_usuario': tipo_usuario,
        }

        if codigo_RFID:
            data['codigo_RFID'] = codigo_RFID
        else:
            data['codigo_RFID'] = "NO_ASIGNADO"

        
        try:
            response = requests.patch(f"{API_URL}/usuarios/{rut}", json=data)  # Change PUT to PATCH
            if response.status_code == 200:
                flash('Usuario actualizado exitosamente.', 'success')
                return redirect(url_for('admin.admin_usuarios'))
            else:
                flash('Error al actualizar el usuario.', 'danger')
        except requests.RequestException as e:
            flash(f'Error al conectar con la API: {e}', 'danger')
            service_offline = True

    return render_template(
        'admin/admin_editar_usuario.html',
        user=g.user,
        usuario=usuario,
        roles=usuario_roles,
        service_offline=service_offline
    )

@admin_bp.route('/eliminar-usuario/<rut>', methods=['POST'])
@role_required('admin')
def eliminar_usuario(rut):
    try:
        response = requests.delete(f"{API_URL}/usuarios/{rut}")
        if response.status_code == 200:
            flash('Usuario eliminado exitosamente.', 'success')
        else:
            flash('Error al eliminar el usuario.', 'danger')
    except requests.RequestException as e:
        flash(f'Error al conectar con la API: {e}', 'danger')
    
    return redirect(url_for('admin.admin_usuarios'))


