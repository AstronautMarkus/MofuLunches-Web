from flask import Blueprint, render_template, session, redirect, url_for, flash

cocineros_bp = Blueprint('cocineros', __name__, url_prefix='/cocineros')

@cocineros_bp.route('/')
def cocineros_index():
    
    user_name = session.get('user_name')
    user_role = session.get('role')

    if not user_name or user_role != "cocineros":
        flash("Acceso denegado. Debes ser cocinero para acceder a esta página.", "error")
        return redirect(url_for('main.index'))

    
    return render_template('cocineros/index.html', user_name=user_name)
