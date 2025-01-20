from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuraciones adicionales, si las hay
    app.config['SECRET_KEY'] = '7778742049'

    # Registrar blueprint
    from .routes import main
    app.register_blueprint(main)
    
    return app
