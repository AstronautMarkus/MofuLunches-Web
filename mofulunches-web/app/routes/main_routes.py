import os
import requests
from flask import Blueprint, render_template, request, jsonify, flash, get_flashed_messages, current_app, session, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

main_bp = Blueprint('main', __name__)


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
    api_url = "http://127.0.0.1:5000/api/usuarios/login" # API URL
    data = request.get_json()

    rut = data.get('username')  # 'username' is 'rut'
    password = data.get('password')

    if not rut or not password:
        return jsonify({"error": "RUT y contraseña son requeridos."}), 400

    try:

        response = requests.post(api_url, json={"rut": rut, "contrasena": password})

        api_data = response.json()

        if response.status_code == 200:
            user_data = api_data['user']
            user_data['role'] = user_data.pop('tipo_usuario')  # 'tipo_usuario' is 'role'

            session['user'] = user_data  # Save data with 'role'
            session['user_name'] = user_data['nombre']
            session['role'] = user_data['role']  # Save role in session
            
            print("Login session:", session)  # DEBUG check session data

            redirect_url = "/admin" if user_data['role'] == "admin" else "/cocineros"
            return jsonify({
                "status": "success",
                "redirect_url": redirect_url,
                "message": "Iniciado sesión exitosamente."
            }), 200
        elif response.status_code == 404:
            return jsonify({"status": "error", "message": "Usuario no encontrado."}), 404
        elif response.status_code == 401:
            return jsonify({"status": "error", "message": "Contraseña incorrecta."}), 401
        else:
            return jsonify({"status": "error", "message": api_data.get('error', 'Error desconocido.')}), response.status_code
    except requests.RequestException as e:
        return jsonify({"status": "error", "message": f"Error de conexión: {str(e)}"}), 500
    except ValueError as ve:
        # Error handling for JSON parsing
        print("Error processing JSON from external API:", str(ve))
        return jsonify({"status": "error", "message": f"Error procesando respuesta de la API: {str(ve)}"}), 500


@main_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  
    flash("Has cerrado sesión.", "success")
    return redirect(url_for('main.index'))

@main_bp.route('/get-flashes', methods=['GET'])
def get_flashes():
    messages = get_flashed_messages(with_categories=True)
    return jsonify([{"category": category, "message": message} for category, message in messages])
