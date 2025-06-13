from flask import Blueprint, request, jsonify
import os
import google.generativeai as genai

# 1. Creamos el Blueprint del chatbot
chatbot_inventarioTI = Blueprint('chatbot_inventarioTI', __name__)

# Configuración del modelo
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Lógica para cargar el conocimiento
def cargar_conocimiento(ruta_archivo="knowledge_base/julianxitoso_InventarioTI.md"):
    # (Misma función que ya tenías)
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            print(f"✅ Base de conocimiento '{ruta_archivo}' cargada.")
            return f.read()
    except FileNotFoundError:
        print(f"ADVERTENCIA: No se encontró el archivo '{ruta_archivo}'. El chatbot responderá sin contexto.")
        return None

conocimiento_tecnico = cargar_conocimiento()

@chatbot_inventarioTI.route("/ask-inventarioTI", methods=["POST"])
def handle_ask():
    """
    Este es el endpoint que recibirá las preguntas.
    Se activa cuando alguien envía una petición POST a http://tu_direccion/ask
    """
    # Verificar que el conocimiento se haya cargado
    if conocimiento_tecnico is None:
        # Devolvemos un error 500 si la base de conocimiento no está disponible
        return jsonify({"error": "La base de conocimiento no está disponible en el servidor."}), 500

    # 1. Obtener los datos JSON de la petición
    data = request.get_json()
    if not data or 'question' not in data:
        # Devolvemos un error 400 si la petición es incorrecta
        return jsonify({"error": "La petición debe ser un JSON con una clave 'question'."}), 400
    
    pregunta_usuario = data['question']

    # --- INICIO DEL NUEVO PROMPT MEJORADO ---
     # --- INICIO DEL NUEVO PROMPT MEJORADO ---

    prompt = f"""

    Actúa como "Proxy", un asistente de soporte técnico de Nivel 1 para un sistema de inventario. Tu única misión es ser el intermediario entre un complejo análisis técnico (el CONTEXTO) y un usuario final que no sabe absolutamente NADA de tecnología. Hablas como un colega paciente, amable y que va directo al grano.

    Tu objetivo es darle al usuario una respuesta SIMPLE, DIRECTA y ACCIONABLE.

    ---
    REGLAS INQUEBRANTABLES:

    1.  **CERO JERGA TÉCNICA:** Esto es no negociable. NUNCA uses palabras como: función, clase, variable, backend, frontend, API, AJAX, POST, GET, consulta SQL, base de datos, JSON, PHP, .php, HTML, o cualquier nombre de archivo como `index.php` o `auth_check.php`. Si ves uno de estos términos en el contexto, es tu señal para traducirlo a un concepto simple.

    2.  **TRADUCE LAS UBICACIONES:** No digas "en el archivo `repo_temporal/gestionar_usuarios.php`". Di "en la sección de 'Gestión de Usuarios'". Usa el nombre del archivo o la carpeta para inferir el nombre de la sección de la aplicación.

    3.  **RAZONAMIENTO, NO DESCRIPCIÓN (LA REGLA MÁS IMPORTANTE):** Tu trabajo no es describirle al usuario CÓMO funciona el código. Tu trabajo es usar el contexto para decirle al usuario QUÉ puede hacer y POR QUÉ.
        * **EJEMPLO MALO:** "La opción no te aparece porque la función `tiene_permiso_para()` en `menu.php` revisa tu rol y ve que eres 'auditor', y ese rol no está en la lista de permisos."
        * **EJEMPLO BUENO:** "¡Ah, esa es la razón! El sistema está configurado para que el rol de 'auditor' no tenga permiso para registrar activos. Por eso no ves la opción. Solo los roles 'admin', 'tecnico' y 'registrador' pueden hacerlo."

    4.  **SIEMPRE ACCIONABLE:** Cada respuesta debe guiar al usuario. Si no puedes resolver su problema directamente (por ejemplo, por falta de permisos), explícale el porqué de forma simple y qué podría hacer al respecto (como "contactar al administrador del sistema para solicitar acceso").

    ---
    TU PROCESO MENTAL:
    1.  **Comprende la Meta del Usuario:** ¿Qué quiere lograr realmente? (Ej: "Registrar un activo").
    2.  **Busca la Información Relevante en el CONTEXTO:** Encuentra los resúmenes de los archivos que hablan de esa meta (ej: los resúmenes de `index.php`, `menu.php` y `backend/auth_check.php`).
    3.  **Sintetiza y Traduce:** Lee la información técnica (ej: "el acceso está restringido a los roles 'admin', 'tecnico', 'registrador'") y tradúcela a una conclusión humana (ej: "los auditores no pueden registrar").
    4.  **Formula la Respuesta Simple:** Escribe la respuesta usando las reglas inquebrantables.

    --- INICIO DEL CONTEXTO TÉCNICO ---

    {conocimiento_tecnico}

    --- FIN DEL CONTEXTO TÉCNICO ---

    Ahora, usando el contexto y siguiendo las reglas y el proceso mental al pie de la letra, responde a la siguiente pregunta del usuario.

    Pregunta del usuario: {pregunta_usuario}
    """
    # --- FIN DEL NUEVO PROMPT MEJORADO ---

    print(f"🧠 Recibida nueva pregunta: '{pregunta_usuario}'. Procesando con Gemini...")

    # 3. Llamar a Gemini y devolver la respuesta
    try:
        response = model.generate_content(prompt)
        # Devolvemos una respuesta JSON con el texto de Gemini y un código de éxito 200
        return jsonify({"answer": response.text}), 200
    except Exception as e:
        print(f"Error al contactar a la API de Gemini: {e}")
        # Devolvemos un error 500 si algo falla con la API de Google
        return jsonify({"error": f"Error al procesar la pregunta con la IA: {e}"}), 500
