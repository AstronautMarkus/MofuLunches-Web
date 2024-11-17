from flask import Blueprint, render_template, session, g

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def before_request():
    g.user = session.get('user')

@admin_bp.route('/')
def admin_index():
    user = session.get('user')  # Get all data in variable
    if not user or user.get("role") != "administrador":
        error_message = "Acceso denegado. Debes ser administrador para acceder a esta página."
        return render_template('error.html', error_message=error_message)

    return render_template('admin/index.html', user=g.user)
