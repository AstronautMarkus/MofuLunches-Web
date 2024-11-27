from flask import Blueprint, render_template, session, g, request, flash, redirect, url_for
from functools import wraps
from dotenv import load_dotenv
import threading
import requests
import serial
import time
import os
from flask_socketio import SocketIO

# Cargar variables de entorno
load_dotenv()
API_URL = os.getenv('API_URL')

# Instancia global de SocketIO
socketio = SocketIO()

# Crear blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador para roles
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
    response = requests.get(f"{API_URL}/usuarios")
    if response.status_code == 200:
        usuarios = response.json()
    else:
        usuarios = []
    return render_template('admin/admin_listar_usuarios.html', user=g.user, usuarios=usuarios)

@admin_bp.route('/crear-usuario', methods=['GET', 'POST'])
@role_required('admin')
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        rut = request.form.get('rut')
        codigo_RFID = request.form.get('codigo_RFID')
        tipo_usuario = request.form.get('tipo_usuario')
        
        data = {
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'contrasena': contrasena,
            'rut': rut,
            'codigo_RFID': codigo_RFID,
            'tipo_usuario': tipo_usuario
        }
        
        response = requests.post(f"{API_URL}/usuarios", json=data)
        
        if response.status_code == 201:
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('admin.admin_usuarios'))
        else:
            try:
                error_message = response.json().get('message', 'Error al crear el usuario')
            except ValueError:
                error_message = 'Error al crear el usuario'
            flash(error_message, 'danger')
    
    return render_template('admin/admin_crear_usuario.html', user=g.user)

# Escuchar el puerto serial para detectar códigos RFID
def serial_listener():
    try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Cambia el puerto según tu configuración
        time.sleep(2)  # Esperar que el Arduino esté listo

        while True:
            if arduino.in_waiting > 0:
                rfid_code = arduino.readline().decode('utf-8').strip()
                print(f"RFID Detectado: {rfid_code}")
                # Emitir el código RFID al cliente a través de SocketIO
                socketio.emit('rfid_detected', {'rfid': rfid_code}, namespace='/admin')
    except serial.SerialException as e:
        print(f"Error al conectar con el puerto serial: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Iniciar hilo para escuchar el puerto serial
def start_serial_listener():
    thread = threading.Thread(target=serial_listener, daemon=True)
    thread.start()
