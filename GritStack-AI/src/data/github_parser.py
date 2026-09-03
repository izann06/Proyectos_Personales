import os
import json
from dotenv import load_dotenv
from github import Github, Auth

def obtener_perfil_github(token: str):
    """
    Se conecta a GitHub y extrae el perfil profesional completo (repositorios originales).
    Devuelve un diccionario con toda la información valiosa estructurada para la IA.
    """
    auth = Auth.Token(token)
    g = Github(auth=auth)
    usuario = g.get_user()
    
    perfil_estructurado = []
    
    for repo in usuario.get_repos():
        if not repo.fork:
            # 1. Intentamos obtener el README
            try:
                readme = repo.get_readme().decoded_content.decode('utf-8')
            except:
                readme = ""
            
            # 2. Recopilamos absolutamente todos los datos que le importan a un reclutador/IA
            datos_repo = {
                "nombre": repo.name,
                "descripcion": repo.description if repo.description else "",
                "url": repo.html_url,
                "etiquetas": repo.get_topics(),
                "lenguajes_bytes": repo.get_languages(),
                "estrellas": repo.stargazers_count,
                "fecha_actualizacion": str(repo.updated_at),
                "readme_texto": readme
            }
            perfil_estructurado.append(datos_repo)
            
    # Devolvemos el paquete completo
    return {
        "usuario": usuario.login,
        "repositorios": perfil_estructurado
    }

# Esta línea significa: "Solo ejecuta lo de abajo si ejecuto este archivo directamente desde la terminal"
if __name__ == "__main__":
    load_dotenv()
    mi_token = os.getenv("GITHUB_TOKEN")
    
    if mi_token:
        print("Extrayendo tu perfil profesional de GitHub... (Esto puede tardar unos segundos)")
        
        # 1. Llamamos a nuestra función maestra
        datos_completos = obtener_perfil_github(mi_token)
        
        # 2. Guardamos el resultado en un archivo JSON para poder leerlo tranquilos
        nombre_archivo = f"perfil_{datos_completos['usuario']}.json"
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            # json.dump escribe los datos de forma bonita (indent=4)
            json.dump(datos_completos, f, ensure_ascii=False, indent=4)
            
        print(f"Exito total! Toda la información de tu perfil se ha guardado en: {nombre_archivo}")
        print("CONSEJO: Busca ese archivo en tu editor y ábrelo para que veas la cantidad de datos que tenemos ahora.")
    else:
        print("Error: No se encontró GITHUB_TOKEN en el archivo .env")
