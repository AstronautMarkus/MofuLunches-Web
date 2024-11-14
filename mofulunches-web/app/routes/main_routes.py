import os
from flask import Blueprint, render_template, request, jsonify, flash, get_flashed_messages, current_app, session, redirect, url_for
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
    if not current_app.secret_key:
        current_app.secret_key = os.getenv('SECRET_KEY')

@main_bp.route('/')
def index():
    user_name = session.get('user_name')
    user_role = session.get('role')
    
    if user_name:
        if user_role == "administrador":
            return redirect(url_for('admin.admin_index'))
        elif user_role == "cocineros":
            return redirect(url_for('cocineros.cocineros_index'))
    
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
                session['user_name'] = username  
                session['role'] = user["role"]  
                redirect_url = "/admin" if user["role"] == "administrador" else "/cocineros"
                return jsonify({"status": "success", "user": username, "role": user["role"], "redirect_url": redirect_url, "message": "Iniciado sesión correctamente!"}), 200
            else:
                return jsonify({"status": "error", "message": "Acceso denegado para el rol requerido. Verifique su rol."}), 403
        else:
            return jsonify({"status": "error", "message": "Contraseña incorrecta."}), 401
    else:
        return jsonify({"status": "error", "message": "Usuario no encontrado."}), 404

@main_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  
    flash("Has cerrado sesión.", "success")
    return redirect(url_for('main.index'))

@main_bp.route('/get-flashes', methods=['GET'])
def get_flashes():
    messages = get_flashed_messages(with_categories=True)
    return jsonify([{"category": category, "message": message} for category, message in messages])
