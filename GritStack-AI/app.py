import streamlit as st
import os

# Configuración básica de la página
st.set_page_config(
    page_title="GritStack AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚀 GritStack AI")
    st.subheader("Plataforma de Inteligencia Profesional")
    
    st.write("---")
    
    st.info("Bienvenido. La arquitectura base ha sido inicializada. La interfaz visual avanzada y los módulos de IA están en construcción. 🛠️")
    
    with st.sidebar:
        st.image("https://img.icons8.com/?size=256&id=114330&format=png", width=100) # Pixel art placeholder
        st.markdown("### Navegación")
        st.button("🏠 Inicio")
        st.button("🔍 Mi Perfil (GitHub)")
        st.button("📄 Mis Documentos")
        st.button("⚙️ Configuración")

if __name__ == "__main__":
    main()
