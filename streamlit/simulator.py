import streamlit as st
import os

st.set_page_config(layout="wide")

st.title("🌌 3D Orbital Telemetry Simulator")
st.caption("Visor interactivo en tiempo real integrado con tu motor gráfico WebGL (Three.js).")

# =========================================================================
# 🔍 RESOLUCIÓN DE RUTAS ABSOLUTAS (Basado en tu raíz de proyecto)
# =========================================================================
# Al estar en 'streamlit/simulator.py', subimos un nivel para encontrar la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "../index.html")
JS_PATH = os.path.join(BASE_DIR, "src", "main.js")
CSS_PATH = os.path.join(BASE_DIR, "styles", "styles.css")

# Verification Blocks en Consola de Desarrollo
if os.path.exists(INDEX_PATH) and os.path.exists(JS_PATH):
    
    # 1. Leer los archivos fuente originales
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
    with open(JS_PATH, "r", encoding="utf-8") as f:
        js_code = f.read()
    
    # 2. Inyectar estilos CSS de forma síncrona si el archivo existe
    css_inline = ""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            css_inline = f"<style>\n{f.read()}\n</style>"
    
    # Reemplazar llamada externa para evitar bloqueos de rutas locales
    html_content = html_content.replace('<link rel="stylesheet" href="../styles/styles.css">', css_inline)

    # 3. Empaquetar y fusionar tu main.js dentro del Bloque de Módulos (importmap)
    # Buscamos tu llamada original del index.html para sustituirla por el código nativo
    script_externo = '<script type="module" src="../src/main.js"></script>'
    
    script_inyectado = f"""
    <script type="module">
        // Código de la aplicación inyectado dinámicamente desde src/main.js
        {js_code}
    </script>
    """
    
    html_final = html_content.replace(script_externo, script_inyectado)

    # 4. Renderizado en Sandbox WebGL Seguro (Previene errores CORS de importmaps)
    # Ajustamos la altura a 750px para dar espacio óptimo a tus paneles de UI
    st.components.v1.html(html_final, height=750, scrolling=False)

else:
    # Bloque de depuración por si el Servidor levanta desde otra ruta base
    st.error("🚨 Error de Enlace: No se pudieron mapear los componentes del simulador.")
    st.info(f"Buscando index.html en: `{INDEX_PATH}`")
    st.info(f"Buscando main.js en: `{JS_PATH}`")