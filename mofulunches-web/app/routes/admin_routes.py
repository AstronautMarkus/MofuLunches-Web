from flask import Blueprint, render_template, session, redirect, url_for, flash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_index():
    user_name = session.get('user_name')
    user_role = session.get('role')

    if not user_name or user_role != "administrador":
        error_message = f"Acceso denegado. Debes ser administrador para acceder a esta página."
        return render_template('error.html', error_message=error_message, user_name=user_name)

    return render_template('admin/index.html', user_name=user_name)
