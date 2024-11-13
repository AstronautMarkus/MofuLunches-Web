import os
from flask import Blueprint, render_template, request, jsonify, flash, get_flashed_messages, current_app
from dotenv import load_dotenv

load_dotenv()

main_bp = Blueprint('main', __name__)

# Users static test
users = {
    "astronautmarkus": {"password": "administrador", "role": "administrador"},
    "sevenjackson": {"password": "cocinero", "role": "cocineros"}
}

@main_bp.before_app_request
def set_secret_key():
    current_app.secret_key = os.getenv('SECRET_KEY')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role_required = data.get('role')

    if username in users:
        user = users[username]
        if user["password"] == password:
            if user["role"] == role_required:
                flash("Login exitoso!", "success")
                return jsonify({"status": "success", "user": username, "role": user["role"]}), 200
            else:
                flash("Acceso denegado para el rol requerido.", "error")
                return jsonify({"status": "error"}), 403
        else:
            flash("Contraseña incorrecta.", "error")
            return jsonify({"status": "error"}), 401
    else:
        flash("Usuario no encontrado.", "error")
        return jsonify({"status": "error"}), 404

@main_bp.route('/get-flashes', methods=['GET'])
def get_flashes():
    messages = get_flashed_messages(with_categories=True)
    return jsonify([{"category": category, "message": message} for category, message in messages])


