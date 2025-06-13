from flask import Blueprint, request, jsonify
import os, git, shutil
import google.generativeai as genai
from git.remote import RemoteProgress
import re
from urllib.parse import urlparse

# 1. Creamos el Blueprint
analyzer_bp = Blueprint('analyzer_bp', __name__)

# Configuración del modelo (asume que las variables de entorno ya están cargadas)
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

def analizar_codigo(contenido_archivo, nombre_archivo):
    #Envia el contenido de un archivo a gemini
    print(f'Analizando el archivo: {nombre_archivo}')
    
     # Creamos un prompt detallado para Gemini
    prompt = f"""
    Eres un programador experto. Analiza el siguiente código del archivo '{nombre_archivo}'.

    Proporcióname un resumen en formato markdown que incluya:
    - Propósito principal del archivo.
    - Descripción de sus funciones o clases.
    - Dependencias clave.

    Aquí está el código:
    ---
    {contenido_archivo}
    ---
    """
    
    try:
        # Hacemos la llamada a la API de Gemini
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al analizar el archivo: {e}"

class CloneProgress(RemoteProgress):
    # (Mismo código que tenías)
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(f'Clonando... {int(cur_count / max_count * 100)}%', end='\r')
        
        
# =======================================================
# ============== FUNCIÓN REAPLICADA ==============
# Esta función convierte una URL de git en un nombre de archivo seguro.
# =======================================================
def url_to_filename(url):
    """Convierte una URL de repositorio en un nombre de archivo seguro."""
    try:
        path = urlparse(url).path
        repo_name = path.strip('/').replace('.git', '')
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', repo_name)
        return f"{safe_name}.md"
    except Exception:
        return f"repo_analisis_{int(os.time.time())}.md"        
        

# 2. La ruta ahora pertenece al Blueprint
@analyzer_bp.route("/analyze", methods=["POST"])

def analyze_repository():
    # TODA la lógica de la función se queda exactamente igual que en api_analyzer.py
    data = request.get_json()
    if not data or 'repo_url' not in data:
        return jsonify({"error": "La petición debe ser un JSON con la clave 'repo_url'."}), 400
    
    repo_url = data['repo_url']
    local_dir = "repo_temporal"

    print(f"Iniciando clonación de {repo_url}...")
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
    git.Repo.clone_from(repo_url, local_dir, progress=CloneProgress())
    print("\nClonación completa.")


    carpetas_excluidas = set(['node_modules', 'vendor', 'dist', 'assets', '.git', 'css','document','fonts','img','js'])
    extensiones_validas = ('.php', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.md', 'Dockerfile')

    analysis_results = [] # Simulación de los resultados
    
    resumen_para_chatbot = f"# Análisis del Repositorio: {repo_url}\n\n"

    for root, dirs, files in os.walk(local_dir):
        dirs[:] = [d for d in dirs if d not in carpetas_excluidas]
        for file in files:
            if file.endswith(extensiones_validas):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if len(content) > 100000:
                            print(f"⏭️  Saltando archivo muy grande: {file_path}")
                            continue
                        
                        analisis_tecnico = analizar_codigo(content, file_path)
                        
                        # Guardar para la respuesta JSON
                        analysis_results.append({
                            "file_path": file_path,
                            "technical_summary": analisis_tecnico
                        })

                        # Guardar para el archivo .md del chatbot
                        resumen_para_chatbot += f"## Archivo: `{file_path}`\n\n{analisis_tecnico}\n\n---\n\n"

                except Exception as e:
                    print(f"No se pudo procesar el archivo {file_path}: {e}")
                    
                    
                    
                    

   # =======================================================
    # ============== LÓGICA DE GUARDADO ÚNICO REAPLICADA ==============
    # =======================================================
    knowledge_dir = "knowledge_base"
    os.makedirs(knowledge_dir, exist_ok=True)
    
    output_filename = url_to_filename(repo_url)
    output_filepath = os.path.join(knowledge_dir, output_filename)

    with open(output_filepath, "w", encoding="utf-8") as f_resumen:
        f_resumen.write(resumen_para_chatbot)
    print(f"✅ Archivo de conocimiento guardado en: '{output_filepath}'")
    
    # Se vuelve a añadir 'knowledge_base' a la respuesta JSON
    return jsonify({
        "status": "Análisis completado",
        "repo_url": repo_url,
        "results": analysis_results,
        "knowledge_base": resumen_para_chatbot
    })