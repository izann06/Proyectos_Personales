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
    
    # 6. Creo un 'set' (conjunto) para guardar las tecnologías sin que se repitan
    tecnologias_usadas = set()
    
    # 6.1 Recorro todos los repositorios que tengo en mi cuenta de GitHub
    repos = usuario.get_repos()
    
    for repo in repos:
        if not repo.fork:
            # 6.2 Obtengo TODOS los lenguajes del proyecto
            lenguajes_del_repo = repo.get_languages()
            
            # lenguajes_del_repo es un diccionario (ej: {'Python': 5000, 'HTML': 200}). 
            # .keys() saca solo los nombres ('Python', 'HTML')
            for lenguaje in lenguajes_del_repo.keys():
                tecnologias_usadas.add(lenguaje)
            
            # 6.3 Busco las etiquetas (topics) del proyecto
            etiquetas = repo.get_topics()
            for etiqueta in etiquetas:
                # Las etiquetas suelen estar en minúscula, las pongo bonitas (ej. 'aws' -> 'Aws')
                tecnologias_usadas.add(etiqueta.title())

    # 7. Imprimo mi lista maestra de tecnologías
    print("🚀 Tecnologías y lenguajes detectados en todo tu GitHub:")
    for tech in tecnologias_usadas:
        print(f" ✅ {tech}")

