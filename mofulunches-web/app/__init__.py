from flask import Flask

def create_app():
    app = Flask(__name__)

   
    app.config.from_object('config.Config')

    # Blueprints
    from .routes.main_routes import main_bp
    from .routes.admin_routes import admin_bp
    from .routes.cocineros_routes import cocineros_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cocineros_bp)

    return app
