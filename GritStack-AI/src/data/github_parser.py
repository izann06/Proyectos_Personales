import os
from dotenv import load_dotenv
from github import Github, Auth

# 1. Cargo las variables del archivo .env
load_dotenv()

# 2. Me guardo el token. os.getenv busca "GITHUB_TOKEN" en el .env
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("❌ Error: No se encontró GITHUB_TOKEN en el archivo .env")
else:
    # 3. Inicio sesión en GitHub usando la forma moderna con Auth
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    
    # 4. Obtengo el usuario autenticado.
    usuario = g.get_user()
    
    # 5. Imprimo el nombre para comprobar que funciona :)
    print(f"✅ ¡Conexión exitosa! Autenticado como: {usuario.login}")

    print("🔍 Analizando tus repositorios...\n")
    
    # 6. Busco en todos mis repositorios
    repos = usuario.get_repos()
    
    # 7. Hago un bucle for para revisar los repositorios uno a uno
    for repo in repos:
        # 7.1 Solo quiero mis proyectos originales (ignoramos los 'forks')
        if not repo.fork:
            nombre = repo.name
            lenguaje = repo.language
            
            # 7.2 Imprimimos el nombre y el lenguaje principal
            print(f"📁 Proyecto: {nombre}")
            print(f"   💻 Lenguaje principal: {lenguaje}")
            print("-" * 30)
