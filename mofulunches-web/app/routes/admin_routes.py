from flask import Blueprint, render_template, session, g
from functools import wraps
import requests
from dotenv import load_dotenv
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
    response = requests.get(f"{API_URL}/usuarios")
    if response.status_code == 200:
        usuarios = response.json()
    else:
        usuarios = []
    return render_template('admin/admin_listar_usuarios.html', user=g.user, usuarios=usuarios)

