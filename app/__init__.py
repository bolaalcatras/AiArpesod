from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os

def create_app():
    # Cargar variables de entorno desde .env al inicio de todo
    load_dotenv()

    # Crear la instancia principal de la aplicación Flask
    app = Flask(__name__)
    CORS(app)
    

    # Importar los blueprints
    from .api_analizador import analyzer_bp
    from .api_chatbot_inventarioTI import chatbot_inventarioTI
    from .api_chatbot_helpdesk import chatbot_helpdesk

    # Registrar los blueprints en la aplicación principal con prefijos de URL
    app.register_blueprint(analyzer_bp, url_prefix='/analyzer')
    app.register_blueprint(chatbot_inventarioTI, url_prefix='/chatbot')
    app.register_blueprint(chatbot_helpdesk, url_prefix='/chatbot')

    @app.route("/")
    def index():
        return "API Modular de Análisis y Chatbot está funcionando."

    return app