from flask import Blueprint, render_template, session, g
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

@admin_bp.route('/usuarios')
@role_required('administrador')
def admin_usuarios():
    return render_template('admin/index.html', user=g.user)