from app import create_app
import os

# Creamos la aplicación usando nuestra fábrica
app = create_app()

if __name__ == '__main__':
    # Usamos un solo puerto, por ejemplo el 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)  
     