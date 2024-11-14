from flask import Blueprint, render_template

cocineros_bp = Blueprint('cocineros', __name__, url_prefix='/cocineros')


@cocineros_bp.route('/')
def admin_index():
    return render_template('cocineros/index.html')

