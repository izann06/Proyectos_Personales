import os
import json
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse

def crear_modelo_ia():
    """
    Crea y devuelve una conexión con Claude Sonnet 4.6 a través de AWS Bedrock.
    """
    load_dotenv()
    
    import boto3
    from botocore.config import Config
    
    config_bedrock = Config(
        connect_timeout=6,
        read_timeout=60,
        retries={'max_attempts': 2}
    )
    
    cliente_bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        config=config_bedrock
    )
    
    modelo = ChatBedrockConverse(
        model="us.anthropic.claude-sonnet-4-6",
        client=cliente_bedrock,
        temperature=0.25,
        max_tokens=4096
    )
    
    return modelo

def generar_readme_ia(datos_perfil: dict) -> str:
    """
    Genera un README.md profesional, con profundidad arquitectónica, pensamiento crítico
    y análisis técnico exhaustivo para el perfil de GitHub del desarrollador usando Claude Sonnet 4.6.
    """
    usuario = datos_perfil.get("usuario", "developer")
    nombre = datos_perfil.get("nombre", usuario)
    bio = datos_perfil.get("bio", "Cloud & DevOps Engineer")
    
    try:
        modelo = crear_modelo_ia()
        datos_texto = json.dumps(datos_perfil, ensure_ascii=False, indent=2)
        
        prompt = f"""Actúa como un Principal Cloud & DevOps Architect y Staff Technical Writer de élite.
Tu misión es transformar el perfil de este ingeniero en un README.md de GitHub con máxima profundidad técnica, pensamiento crítico y excelencia visual.

DIRECTRICES CLAVE DE CONTENIDO & PENSAMIENTO CRÍTICO:
1. ESPECIALIZACIÓN ROTUNDA: El ingeniero es **Cloud & DevOps Engineer / SRE**.
   - Prohibido utilizar clichés corporativos vacíos ("apasionado por la tecnología", "entusiasta del código", "siempre buscando nuevos retos").
   - Sustituye generalidades por decisiones de arquitectura, trade-offs técnicos y justificaciones de diseño.
2. ANÁLISIS ARQUITECTÓNICO DE SUS 3 PROYECTOS INSIGNIA:
   - **AWS Serverless Text-to-Speech (IaC con Terraform)**:
     * Arquitectura reactiva y desacoplada mediante S3 Event Notifications disparando AWS Lambda (stateless execution).
     * Gestión completa del ciclo de vida de infraestructura mediante Terraform HCL, garantizando estado reproducible y cero drift a coste 0€ bajo AWS Free Tier.
     * Seguridad estricta con políticas IAM de Mínimo Privilegio (Least Privilege) limitando permisos exclusivamente a polly:SynthesizeSpeech y prefijos específicos de S3.
     * Incluye un diagrama de arquitectura conciso en bloque de texto/ASCII.
   - **Docker Labs & Homelab Infrastructure (Orquestación & Zero-Trust)**:
     * Orquestación de microservicios con Docker Compose: separación en redes internas tipo puente (Zero-Trust bridge networks) donde las bases de datos (PostgreSQL, Redis) no exponen puertos al host.
     * Estrategias de persistencia con Named Volumes y healthchecks para resolución de dependencias (service_healthy).
   - **DevOps Proyectos & Linux Automation Roadmap**:
     * Ingeniería de sistemas y observabilidad en Linux: scripts modulares en Bash analizando métricas de /proc, CPU, saturación de I/O y memoria.
     * Workflows de CI/CD en GitHub Actions para validación sintáctica y pruebas automatizadas.
3. ESTILO Y FORMATO:
   - Inicia directamente con `# ` y el nombre del desarrollador.
   - En los 3 proyectos destacados, el título y enlace deben ir OBLIGATORIAMENTE en la misma línea del número con este formato exacto:
     `#### 1. [🎙️ AWS Serverless Text-to-Speech (IaC con Terraform)](https://github.com/{usuario}/aws-serverless-text-to-speech)`
     `#### 2. [🐳 Docker Labs & Homelab Infrastructure (Orquestación & Zero-Trust)](https://github.com/{usuario}/Docker-Labs)`
     `#### 3. [⚙️ DevOps Proyectos & Linux Systems Automation](https://github.com/{usuario}/DevOps-Proyectos-RoadMap)`
     (Prohibido dejar el número solo como '1.' o '#### 1.' en una línea separada).
   - Badges sobrios y fiables de shields.io con style=for-the-badge (AWS, Terraform, Docker, Linux, Bash, GitHub Actions, Python, C#).
     Para Terraform usa exactamente: `https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white`
   - En la sección '### 📊 Métricas de Ingeniería en GitHub', incluye los 4 badges centrados (Repositorios Públicos, Estrellas Totales, Especialidad Cloud & DevOps e Infraestructura AWS & Docker).
   - Prohibidas imágenes de servidores externos inestables (NO uses vercel.app ni herokuapp).
   - Sección de contacto elegante con GitHub y LinkedIn.

<contrato_de_salida>
- Responde ÚNICAMENTE con el Markdown del README.
- Cero comentarios, intros o explicaciones fuera del markdown.
- Primer carácter: '# '.
</contrato_de_salida>

DATOS REALES DEL PERFIL:
{datos_texto}
"""
        respuesta = modelo.invoke(prompt)
        contenido = respuesta.content
        if isinstance(contenido, list):
            contenido = "".join(item.get("text", "") if isinstance(item, dict) else str(item) for item in contenido)
        return str(contenido).strip()
    except Exception as e:
        print(f"[Fallback README] {e}")
        # Fallback de alta fidelidad arquitectónica para Izan
        return f"""# {nombre} (@{usuario}) 👋

> 🚀 **Cloud & DevOps Engineer** | AWS · Terraform (IaC) · Docker · CI/CD · Linux Systems
> *Especializado en arquitecturas reactivas serverless, orquestación de contenedores y automatización de infraestructura como código bajo el principio de menor privilegio.*

---

### ☁️ Stack Tecnológico & Especialización

<div align="left">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS" />
  <img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="CI/CD" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Bash" />
  <img src="https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=c-sharp&logoColor=white" alt="C#" />
</div>


---

### 🏛️ Arquitectura & Proyectos Destacados

#### 1. [🎙️ AWS Serverless Text-to-Speech (IaC con Terraform)](https://github.com/{usuario}/aws-serverless-text-to-speech)
Arquitectura reactiva en **AWS** orquestada al 100% mediante **Terraform (IaC)**:
- **Flujo de Eventos:** `S3 Bucket (Input) ──> S3 Event Trigger ──> AWS Lambda (Python) ──> Amazon Polly (TTS) ──> S3 (Output Audio)`
- **Diseño de Seguridad:** Políticas IAM con el Principio de Menor Privilegio (Least Privilege), restringiendo el scope de Lambda a `polly:SynthesizeSpeech` y lectura/escritura en prefijos específicos de S3.
- **Reproducibilidad:** Control de estado declarativo sin intervención manual en la consola web, manteniendo un coste operativo de **0.00€** bajo la capa gratuita.
*Tech Stack: `AWS Lambda` · `Terraform HCL` · `Amazon Polly` · `Amazon S3` · `IAM Least Privilege` · `Python`*

#### 2. [🐳 Docker Labs & Homelab Infrastructure](https://github.com/{usuario}/Docker-Labs)
Entorno de pruebas y orquestación multicontenedor con **Docker Compose**:
- **Topología Zero-Trust:** Redes privadas tipo puente (bridge networks) con aislamiento estricto. Las bases de datos (`PostgreSQL`, `Redis`) no exponen puertos al host y solo se comunican a través de DNS interno con las APIs (`FastAPI`, `Node.js`).
- **Resiliencia & Persistencia:** Named Volumes desacoplados del ciclo de vida del contenedor y healthchecks (`depends_on: condition: service_healthy`) para garantizar disponibilidad de dependencias.
*Tech Stack: `Docker` · `Docker Compose` · `FastAPI` · `PostgreSQL` · `Redis` · `Portainer`*

#### 3. [⚙️ DevOps Proyectos & Linux Systems Automation](https://github.com/{usuario}/DevOps-Proyectos-RoadMap)
Ingeniería de sistemas, automatización de tareas y pipelines de entrega continua:
- **Diagnóstico de Sistemas:** Scripts modulares en Bash para inspección proactiva de recursos en servidores Linux (`/proc`, saturación de memoria, métricas de disco e interfaces de red).
- **CI/CD & Hardening:** Workflows automatizados con GitHub Actions para linting de código, gestión de llaves criptográficas SSH y despliegue de proxies inversos seguros con Nginx.
*Tech Stack: `Bash Scripting` · `Linux Systems` · `GitHub Actions` · `Nginx` · `SSH Hardening`*

---

### 📊 Métricas de Ingeniería en GitHub
<div align="center">
  <img src="https://img.shields.io/badge/Repositorios_Publicos-{len(datos_perfil.get('repositorios', []))}-232F3E?style=for-the-badge&logo=github&logoColor=white" alt="repos"/>
  <img src="https://img.shields.io/badge/Estrellas_Totales-{datos_perfil.get('estadisticas', {}).get('total_estrellas', 0)}-f59e0b?style=for-the-badge&logo=apachespark&logoColor=white" alt="stars"/>
  <img src="https://img.shields.io/badge/Especialidad-Cloud_%26_DevOps-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="focus"/>
  <img src="https://img.shields.io/badge/Infraestructura-AWS_%26_Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="docker"/>
</div>


---

### 📫 Contacto Profesional
- 💼 **LinkedIn:** [Izan Marcos Martínez](https://www.linkedin.com/in/izan-marcos-mart%C3%ADnez-913728369)
- 🌐 **GitHub:** [@{usuario}](https://github.com/{usuario})
- 📍 **Ubicación:** {datos_perfil.get('ubicacion', 'España')}
"""

def responder_chat_ia(pregunta: str, datos_perfil: dict, historial: list = None) -> str:
    """
    Responde consultas actuando como Principal Cloud & DevOps Architect y Mentor Técnico de élite,
    aportando pensamiento crítico, análisis de trade-offs y recomendaciones de ingeniería avanzadas.
    """
    try:
        modelo = crear_modelo_ia()
        usuario = datos_perfil.get("usuario", "desarrollador")
        nombre = datos_perfil.get("nombre", usuario)
        
        prompt = f"""Eres un Principal Cloud & DevOps Architect y Staff Engineer Mentor de élite en GritStack AI.
Estás asesorando técnicamente a {nombre} (@{usuario}).

CONOCIMIENTO DEL PERFIL TÉCNICO DE {nombre}:
- Especialidad: **CLOUD COMPUTING, DEVOPS, INFRAESTRUCTURA COMO CÓDIGO (IaC) Y SISTEMAS DISTRIBUIDOS**.
- Proyectos insignia reales:
  1. 'aws-serverless-text-to-speech': S3 Event Notifications -> AWS Lambda -> Amazon Polly. Infraestructura provisionada con Terraform HCL, políticas IAM Least Privilege.
  2. 'Docker-Labs': Redes privadas Zero-Trust en Docker Compose, Named Volumes, microservicios FastAPI, PostgreSQL y Redis sin exposición de puertos al host.
  3. 'DevOps-Proyectos-RoadMap': Automatización Linux en Bash (/proc, métricas), Nginx hardening y CI/CD con GitHub Actions.

REGLAS DE RESPUESTA (PENSAMIENTO CRÍTICO & PROFUNDIDAD TÉCNICA):
1. CERO CLICHÉS: Evita respuestas genéricas o de autoayuda técnica.
2. TRADE-OFFS REALES: Cuando recomiendes una herramienta o patrón, explica pros, contras y trade-offs arquitectónicos (ej. Serverless vs Contenedores; Terraform vs OpenTofu; Docker Compose en desarrollo vs Kubernetes con Helm en producción; S3+DynamoDB state locking vs Terraform Cloud).
3. CRITERIO SENIOR: Si te pregunta qué estudiar o cómo mejorar, dale una hoja de ruta con prioridades de ingeniería sólidas: Observabilidad (Prometheus, Grafana, OpenTelemetry), Kubernetes HA (Pods, Deployments, Ingress, Cert-Manager), Gestión de Secretos (AWS Secrets Manager / Vault) y Seguridad DevSecOps (Trivy, SonarQube).
4. SÉ DIRECTO Y RIGUROSO.

Pregunta del ingeniero {nombre}:
"{pregunta}"
"""
        respuesta = modelo.invoke(prompt)
        contenido = respuesta.content
        if isinstance(contenido, list):
            contenido = "".join(item.get("text", "") if isinstance(item, dict) else str(item) for item in contenido)
        return str(contenido).strip()
    except Exception as e:
        print(f"[Fallback Chat] {e}")
        p_lower = pregunta.lower()
        if "fortaleza" in p_lower or "fuerte" in p_lower:
            return "Tus 3 mayores fortalezas técnicas analizadas desde un punto de vista de arquitectura son:\n\n1. **Infraestructura como Código (IaC) Declarativa en AWS**: Has diseñado una arquitectura reactiva serverless (S3 -> Lambda -> Polly) orquestada íntegramente con Terraform, aplicando el principio de menor privilegio en IAM y garantizando coste 0€.\n2. **Seguridad y Topología en Contenedores**: En tu repositorio 'Docker-Labs' implementas aislamiento de red Zero-Trust en Compose (bases de datos no expuestas al host) y persistencia resiliente mediante Named Volumes.\n3. **Ingeniería de Sistemas y Automatización Base**: Dominio de scripting en Bash sobre entornos Linux (/proc, monitorización de I/O y memoria) y pipelines CI/CD automatizados en GitHub Actions."
        elif "entrevista" in p_lower or "proyecto" in p_lower:
            return "En entrevistas técnicas para puestos Cloud/DevOps, tu proyecto de referencia debe ser **`aws-serverless-text-to-speech`**:\n- **El problema:** Síntesis de voz escalable sin incurrir en costes de infraestructura ociosa.\n- **La arquitectura:** Event-driven architecture con triggers S3 hacia Lambda en Python.\n- **El trade-off:** Optaste por Terraform para el control estricto del estado (`tfstate`) y reproducibilidad en lugar de configuraciones ad-hoc en la consola web de AWS.\n- **Seguridad:** Políticas IAM estrictamente acotadas a `polly:SynthesizeSpeech`."
        else:
            return "Para dar el salto a un perfil Senior tras consolidar Terraform y Docker Compose, la ruta crítica de ingeniería debe ser:\n\n1. **Orquestación en Producción (Kubernetes - K8s)**: Arquitectura de control plane/workers, Deployments, Services, Ingress Controllers y empaquetado con **Helm**.\n2. **Observabilidad Distribuida**: Métricas con **Prometheus**, dashboards en **Grafana** y trazas con **OpenTelemetry**.\n3. **DevSecOps**: Escaneo de vulnerabilidades en imágenes de contenedores con **Trivy** y análisis estático de código IaC con **tfsec** o **Checkov**."

