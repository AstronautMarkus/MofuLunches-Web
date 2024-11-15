from flask import Blueprint, render_template, session, redirect, url_for, flash

cocineros_bp = Blueprint('cocineros', __name__, url_prefix='/cocineros')

@cocineros_bp.route('/')
def cocineros_index():
    user = session.get('user')  # Get all data in variable
    if not user or user.get("role") != "cocineros":
        error_message = "Acceso denegado. Debes ser cocinero para acceder a esta página."
        return render_template('error.html', error_message=error_message)

    return render_template('cocineros/index.html', user=user)
