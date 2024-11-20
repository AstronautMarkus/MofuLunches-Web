from flask import Blueprint, render_template, session, g, jsonify, request
from functools import wraps

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
@role_required('administrador')
def admin_index():
    return render_template('admin/index.html', user=g.user)

@admin_bp.route('/usuarios-list')
@role_required('administrador')
def admin_usuarios():
    usuarios = [
        {"id": 1, "nombre": "Juan", "apellidos": "Pérez", "rut": "12345678-9", "rol": "admin", "rfid": "A1B2C3D4"},
        {"id": 2, "nombre": "Ana", "apellidos": "González", "rut": "87654321-0", "rol": "cocinero", "rfid": "E5F6G7H8"},
        {"id": 3, "nombre": "Carlos", "apellidos": "Ramírez", "rut": "22334455-6", "rol": "empleado", "rfid": "I9J0K1L2"},
        {"id": 4, "nombre": "María", "apellidos": "Fernández", "rut": "66778899-1", "rol": "empleado", "rfid": "M3N4O5P6"},
        {"id": 5, "nombre": "Luis", "apellidos": "Martínez", "rut": "99887766-5", "rol": "admin", "rfid": "Q7R8S9T0"},
        {"id": 6, "nombre": "Sofía", "apellidos": "López", "rut": "11223344-7", "rol": "empleado", "rfid": "U1V2W3X4"},
        {"id": 7, "nombre": "Pedro", "apellidos": "Gómez", "rut": "55667788-2", "rol": "empleado", "rfid": "Y5Z6A7B8"},
        {"id": 8, "nombre": "Laura", "apellidos": "Hernández", "rut": "33445566-7", "rol": "empleado", "rfid": "C9D0E1F2"},
        {"id": 9, "nombre": "Miguel", "apellidos": "Torres", "rut": "44556677-8", "rol": "empleado", "rfid": "G3H4I5J6"},
        {"id": 10, "nombre": "Elena", "apellidos": "Morales", "rut": "55667788-9", "rol": "empleado", "rfid": "K7L8M9N0"},
        {"id": 11, "nombre": "Jorge", "apellidos": "Vargas", "rut": "66778899-0", "rol": "empleado", "rfid": "O1P2Q3R4"},
        {"id": 12, "nombre": "Patricia", "apellidos": "Castro", "rut": "77889900-1", "rol": "empleado", "rfid": "S5T6U7V8"},
        {"id": 13, "nombre": "Raúl", "apellidos": "Mendoza", "rut": "88990011-2", "rol": "empleado", "rfid": "W9X0Y1Z2"},
        {"id": 14, "nombre": "Gabriela", "apellidos": "Rojas", "rut": "99001122-3", "rol": "empleado", "rfid": "A3B4C5D6"},
        {"id": 15, "nombre": "Fernando", "apellidos": "Silva", "rut": "00112233-4", "rol": "empleado", "rfid": "E7F8G9H0"}
    ]
    return render_template('admin/admin_listar_usuarios.html', user=g.user, usuarios=usuarios)

