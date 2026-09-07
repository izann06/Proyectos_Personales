"""
Servicio de Selección y Curaduría de Proyectos Top de GitHub.
Filtra y selecciona los 3 proyectos de mayor impacto y relevancia técnica (especialmente Cloud & DevOps).
"""

def seleccionar_top_proyectos(datos_perfil: dict) -> list:
    """
    Selecciona los 3 mejores proyectos del desarrollador priorizando calidad técnica,
    arquitectura Cloud/DevOps, presencia de documentación y relevancia.
    """
    repos = datos_perfil.get("repositorios", [])
    if not repos:
        return []

    # Proyectos insignia pre-curados si coinciden con el perfil de Izan
    insignia_conocidos = {
        "aws-serverless-text-to-speech": {
            "nombre": "AWS Serverless Text-to-Speech",
            "tagline": "Arquitectura Cloud Serverless & Terraform (IaC)",
            "descripcion": "Infraestructura como Código (IaC) completa en AWS con Terraform. Orquesta S3, AWS Lambda (Python), Amazon Polly y políticas estrictas de menor privilegio en IAM a coste 0€.",
            "stack": ["AWS Lambda", "Terraform", "Python", "Amazon Polly", "S3", "IAM"],
            "url": "https://github.com/izann06/aws-serverless-text-to-speech",
            "categoria": "Cloud & IaC",
            "icono": "☁️",
            "estrellas": 0
        },
        "docker-labs": {
            "nombre": "Docker Labs & Homelab Playground",
            "tagline": "Orquestación Multicontenedor y Redes Zero-Trust",
            "descripcion": "Laboratorio integral de contenedores Docker y Compose: microservicios con FastAPI y Node.js, persistencia con volúmenes, Redis, PostgreSQL y automatización con n8n y Portainer.",
            "stack": ["Docker", "Docker Compose", "FastAPI", "PostgreSQL", "Redis", "Portainer"],
            "url": "https://github.com/izann06/Docker-Labs",
            "categoria": "DevOps & Containers",
            "icono": "🐳",
            "estrellas": 0
        },
        "devops-proyectos-roadmap": {
            "nombre": "DevOps Roadmap & Linux Automation",
            "tagline": "Scripting de Servidores, CI/CD y Hardening",
            "descripcion": "Prácticas de ingeniería de sistemas y DevOps: scripts Bash para análisis de rendimiento en Linux, despliegues automáticos con GitHub Actions y gestión de accesos seguros SSH.",
            "stack": ["Bash / Shell", "Linux", "GitHub Actions", "Nginx", "CI/CD", "SSH"],
            "url": "https://github.com/izann06/DevOps-Proyectos-RoadMap",
            "categoria": "Systems & CI/CD",
            "icono": "⚙️",
            "estrellas": 0
        }
    }

    # Buscar si existen estos proyectos en los repositorios del usuario
    top_seleccionados = []
    repos_dict = {r.get("nombre", "").lower(): r for r in repos}

    for key, info in insignia_conocidos.items():
        if key in repos_dict:
            repo_real = repos_dict[key]
            # Conservar o enriquecer con datos en tiempo real
            info["estrellas"] = repo_real.get("estrellas", 0)
            top_seleccionados.append(info)

    # Si encontramos los 3 top específicos, devolverlos inmediatamente
    if len(top_seleccionados) >= 3:
        return top_seleccionados[:3]

    # Si no es Izan o faltan proyectos, aplicamos algoritmo de scoring inteligente
    candidatos = []
    keywords_cloud_devops = ["docker", "terraform", "aws", "cloud", "serverless", "devops", "ci", "cd", "action", "linux", "nginx", "k8s"]

    for r in repos:
        nombre = r.get("nombre", "")
        # Ignorar repositorios especiales de notas o perfiles
        if nombre.lower() in [datos_perfil.get("usuario", "").lower(), "apuntes-tecnicos-obsidian", "portfolio", "1dam", "2dam"]:
            continue

        desc = r.get("descripcion", "") or ""
        readme = r.get("readme_texto", "") or ""
        stars = r.get("estrellas", 0)
        langs = list(r.get("lenguajes_bytes", {}).keys())

        # Cálculo de puntuación técnica
        score = stars * 10
        if len(readme) > 400:
            score += 15
        if desc:
            score += 5
            
        texto_busqueda = (nombre + " " + desc + " " + readme).lower()
        coincidencias = sum(1 for kw in keywords_cloud_devops if kw in texto_busqueda)
        score += coincidencias * 8

        stack = langs[:4] if langs else ["Software"]
        candidatos.append({
            "score": score,
            "data": {
                "nombre": nombre,
                "tagline": desc[:65] + "..." if len(desc) > 65 else (desc or "Proyecto de desarrollo"),
                "descripcion": desc or "Proyecto con arquitectura modular y código versionado en GitHub.",
                "stack": stack,
                "url": r.get("url", f"https://github.com/{datos_perfil.get('usuario')}/{nombre}"),
                "categoria": "DevOps & Cloud" if coincidencias > 0 else "Software Engineering",
                "icono": "🚀",
                "estrellas": stars
            }
        })

    candidatos.sort(key=lambda x: x["score"], reverse=True)
    
    # Rellenar hasta tener 3
    for cand in candidatos:
        if not any(item["nombre"] == cand["data"]["nombre"] for item in top_seleccionados):
            top_seleccionados.append(cand["data"])
            if len(top_seleccionados) == 3:
                break

    return top_seleccionados[:3]
