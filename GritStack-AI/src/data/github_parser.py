import os
import json
from dotenv import load_dotenv
from github import Github, Auth

def obtener_perfil_github(token: str):
    """
    Se conecta a GitHub y extrae el perfil profesional completo (repositorios originales).
    Devuelve un diccionario con toda la información valiosa estructurada para la IA.
    Si hay un fallo puntual de conexión a la API, recurre a la caché local existente.
    """
    try:
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
                langs = repo.get_languages() or {}
                langs_clean = {k: v for k, v in langs.items() if isinstance(v, int) and k.lower() != "url"}
                
                datos_repo = {
                    "nombre": repo.name,
                    "descripcion": repo.description if repo.description else "",
                    "url": repo.html_url,
                    "etiquetas": repo.get_topics(),
                    "lenguajes_bytes": langs_clean,
                    "estrellas": repo.stargazers_count,
                    "fecha_actualizacion": str(repo.updated_at),
                    "readme_texto": readme
                }
                perfil_estructurado.append(datos_repo)
                
        # Estadísticas agregadas
        total_estrellas = sum(r.get("estrellas", 0) for r in perfil_estructurado)
        
        # Lenguajes agregados
        lenguajes_totales = {}
        for r in perfil_estructurado:
            for lang, b in r.get("lenguajes_bytes", {}).items():
                if isinstance(b, int) and lang.lower() != "url":
                    lenguajes_totales[lang] = lenguajes_totales.get(lang, 0) + b
                
        total_bytes = sum(lenguajes_totales.values()) or 1
        lenguajes_top = [
            {
                "nombre": lang,
                "bytes": b,
                "porcentaje": round((b / total_bytes) * 100, 1)
            }
            for lang, b in sorted(lenguajes_totales.items(), key=lambda x: x[1], reverse=True)[:6]
        ]

        resultado = {
            "usuario": usuario.login,
            "nombre": usuario.name or usuario.login,
            "avatar_url": usuario.avatar_url or "https://avatars.githubusercontent.com/u/105436660?v=4",
            "bio": usuario.bio or "Desarrollador Junior Fullstack en transición hacia Cloud & DevOps.",
            "seguidores": usuario.followers,
            "siguiendo": usuario.following,
            "url_perfil": usuario.html_url,
            "ubicacion": usuario.location or "Remoto / España",
            "empresa": usuario.company or "",
            "estadisticas": {
                "total_repositorios": len(perfil_estructurado),
                "total_estrellas": total_estrellas,
                "lenguajes_top": lenguajes_top
            },
            "repositorios": perfil_estructurado
        }

        # Guardamos en caché local para máxima resiliencia
        try:
            with open(f"perfil_{usuario.login}.json", "w", encoding="utf-8") as f_out:
                json.dump(resultado, f_out, ensure_ascii=False, indent=4)
        except:
            pass

        return resultado

    except Exception as e:
        # Recuperación inteligente desde caché si hay fallo de red o timeout
        archivos_cache = [f for f in os.listdir(".") if f.startswith("perfil_") and f.endswith(".json")]
        if archivos_cache:
            with open(archivos_cache[0], "r", encoding="utf-8") as f:
                datos_cache = json.load(f)
                return datos_cache
        raise e

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
