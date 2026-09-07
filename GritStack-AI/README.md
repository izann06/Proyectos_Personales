<div align="center">
  <h1>🚀 GritStack AI</h1>
  <p><strong>Plataforma de Inteligencia Profesional impulsada por IA</strong></p>
  <p><em>Analiza evidencia real de tu trayectoria, detecta carencias y optimiza tu perfil.</em></p>
</div>

---

## 📌 ¿Qué estamos construyendo?

**GritStack AI** no es el típico generador de currículums. Es una plataforma inteligente que en lugar de preguntarte "qué sabes hacer", **demuestra** lo que sabes hacer analizando tus datos reales.

Usando Inteligencia Artificial Avanzada (Modelos RAG y AWS Bedrock), la plataforma lee tu código, tus certificados y tu perfil, y te ayuda a trazar la ruta exacta hacia el trabajo de tus sueños.

### 🌟 Funcionalidades Estrella
1. **Analizador de Evidencias**: Conecta tu GitHub o sube tus certificados y la IA extraerá tus *skills* reales.
2. **Skill Gap Analysis**: ¿Quieres ser *Cloud Engineer*? La IA compara tu perfil actual con las ofertas de trabajo reales y te dice exactamente qué te falta aprender.
3. **Generador de CVs Anti-ATS**: Crea un currículum distinto para cada oferta de trabajo, asegurando que contiene las palabras clave necesarias.
4. **Roadmap Personalizado**: Genera un plan de estudio paso a paso para alcanzar tus metas.

---

## 🏗️ Estructura del Proyecto

Esta es la organización de nuestro código para mantener todo limpio y escalable:

```text
GritStack-AI/
├── app.py                 # 🚀 Punto de entrada principal (Streamlit)
├── requirements.txt       # 📦 Dependencias de Python necesarias
├── .env.example           # 🔑 Plantilla para variables de entorno (AWS, GitHub)
├── README.md              # 📖 Este documento explicativo
│
├── src/                   # 🧠 El corazón de la aplicación
│   ├── config/            # Configuraciones generales, estilos y constantes
│   ├── core/              # Lógica de Inteligencia Artificial (LangChain, Prompts)
│   ├── data/              # Ingesta de datos (Conexión GitHub, Lectura PDFs)
│   ├── database/          # Conexión con bases de datos (ChromaDB, DynamoDB)
│   └── ui/                # Componentes visuales y páginas de Streamlit
│
└── assets/                # 🎨 Imágenes, iconos pixel art y estilos CSS
```

---

## 🛠️ Tecnologías

*   **Frontend**: Streamlit (Python) - Para una interfaz limpia, interactiva y "Glassmorphism".
*   **Inteligencia Artificial**: LangChain + Amazon Bedrock (Claude 3 / Titan).
*   **Base de Datos**: ChromaDB (Vectores) y AWS DynamoDB (Perfiles).
*   **Almacenamiento**: Amazon S3.

---

## 🔑 Configuración del `.env`

Para que la aplicación se conecte con los servicios externos, necesitas crear tu archivo `.env` y rellenarlo. Aquí te explico dónde conseguir cada clave:

### 1. `GITHUB_TOKEN`
- Entra a GitHub y ve a **Settings > Credentials > Personal access tokens**.
- Haz clic en **Generate new token (classic)**.
- Dale un nombre (ej. `GritStack`) y marca los permisos **`repo`** y **`read:user`**.
- Cópialo y pégalo en tu `.env`.

### 2. AWS Credentials
- Inicia sesión en la consola de AWS y ve a **IAM (Identity and Access Management)**.
- En **Users**, crea uno nuevo. En la pantalla de establecer permisos, elige la tercera opción: **"Adjuntar políticas directamente"**. Luego, busca en la barra inferior y marca el check de estas tres políticas: `AmazonBedrockFullAccess`, `AmazonDynamoDBFullAccess` y `AmazonS3FullAccess`.
- Entra dentro de tu usuario y en la pestaña **Security credentials**, dale a **Create access key** y dale a **Codigo local**.
- Copia tu **Access Key ID** y tu **Secret Access Key** al `.env`.
- En `AWS_REGION` escribe la región que estés usando (normalmente `us-east-1` o `us-west-2`).

---

## 💻 Instalación y Entorno Virtual (venv)

Para ejecutar este proyecto de forma segura, utilizamos un **Entorno Virtual (`venv`)**. Esto es como una "caja aislada" que evita que las librerías de este proyecto entren en conflicto con otros proyectos de tu ordenador.

Sigue estos pasos en tu terminal (en la raíz del proyecto):

1. **Crear el entorno virtual:**
   ```bash
   python -m venv venv
   ```
2. **Activar el entorno:**
   - En Windows: `.\venv\Scripts\activate`
   *(Sabrás que está activo si ves un `(venv)` al principio de tu terminal, aunque algunas terminales modernas como Warp pueden ocultarlo).*
3. **Instalar las dependencias:**
   `pip` es el instalador de paquetes de Python. Le diremos que lea nuestra "lista de la compra" (`requirements.txt`) e instale todo dentro del entorno aislado:
   ```bash
   pip install -r requirements.txt
   ```
4. **Probar la conexión inicial:**
   Para comprobar que todo está bien configurado y el token funciona, ejecutamos el script de prueba:
   ```bash
   python src/data/github_parser.py
   ```
   *¿Qué hace este script exactamente?* Este código lee tu clave secreta del `.env` de forma segura, se conecta a los servidores de GitHub usando el método de autenticación moderna (`Auth.Token`) y te devuelve tu nombre de usuario. Si ves un mensaje diciendo `✅ ¡Conexión exitosa! Autenticado como: ...`, significa que la aplicación ya tiene permiso para leer tu código y repositorios como si fueras tú. ¡Magia! ✨

---

## 🗺️ Diario de Desarrollo (Roadmap)

Construir una plataforma de Inteligencia Artificial desde cero no es tarea fácil. Aquí documento mi viaje, fase a fase, con sus objetivos, retos superados y los hitos alcanzados. ¡Acompáñame en el proceso!

### ⚙️ Fase 0: Arquitectura y Cimientos
* **🎯 Objetivo:** Establecer una base sólida, segura y escalable para el proyecto. 
* **🚧 Retos / Inconvenientes:** Entender cómo aislar el proyecto para no mezclar librerías y configurar la seguridad de los tokens para no exponer datos sensibles en internet.
* **✅ Lo que he logrado:**
  - Creación del entorno virtual (`venv`) para el aislamiento de dependencias.
  - Implementación del archivo `.env` para proteger las credenciales (AWS y GitHub).
  - Estructuración profesional de carpetas siguiendo el patrón `src/core`, `src/data`, `src/ui`.

---

### 🐙 Fase 1: Extracción de Evidencias (GitHub Parser)
* **🎯 Objetivo:** Conectar Python con GitHub para descargar toda mi trayectoria como programador (repositorios, lenguajes, fechas, descripciones y READMEs).
* **🚧 Retos / Inconvenientes:** GitHub a veces clasifica erróneamente tecnologías (ej: detecta un `.url` o un `Batchfile` como lenguaje de programación importante). Además, imprimir emojis (`⏳`, `✅`) en la consola de Windows causaba cierres inesperados por problemas de codificación (`UnicodeEncodeError`).
* **✅ Lo que he logrado:**
  - Script automatizado que limpia y filtra los repositorios basura o *forks*.
  - Generación de un archivo `perfil_izann06.json` estructurado con la información pura, listo para ser consumido por la IA.
  - Resolución de errores de codificación en terminales Windows.

---

### 🧠 Fase 2: El Cerebro de la Operación (LangChain + AWS Bedrock)
* **🎯 Objetivo:** Enviar el inmenso JSON generado en la Fase 1 a un modelo fundacional avanzado (Claude 3) para que extraiga insights reales y evalúe mis verdaderas *skills*.
* **🚧 Retos / Inconvenientes:** La arquitectura de Amazon Bedrock cambió para los nuevos modelos (como Claude 4.6), exigiendo usar *Inference Profiles* (`us.anthropic.claude-sonnet-4-6`) en lugar de llamar al modelo por su nombre a secas. Además, la IA generaba informes tan visuales (con emojis) que rompía de nuevo la consola al intentar imprimirlos.
* **✅ Lo que he logrado:**
  - Conexión exitosa a **Claude Sonnet 4.6** a través de **AWS Bedrock** y **LangChain**.
  - Creación de un script (`listar_modelos.py`) para explorar el catálogo de IA disponible en tiempo real en AWS.
  - *Prompt Engineering* avanzado para obligar a la IA a ser objetiva y no inventar habilidades.
  - Guardado automatizado del análisis en formato `.md` (`informe_profesional.md`) para facilitar su lectura.

---

### 🚀 Fase 3: Interfaz Gráfica & Dashboard Glassmorphism (Streamlit)
* **🎯 Objetivo:** Envolver el motor analítico en una aplicación web interactiva de alto impacto estético, moderna y responsiva.
* **🚧 Retos / Inconvenientes:** Streamlit por defecto aplica estilos estándar y colores planos. Fue necesario inyectar CSS puro con `glassmorphism`, tipografía sans-serif geométrica moderna (Google Fonts *Outfit* y *Plus Jakarta Sans*) y controlar los anchos y eventos de pestañas para evitar desbordamientos y enlaces rotos.
* **✅ Lo que he logrado:**
  - Sistema de diseño completo en Dark Mode (`#0b0f19`) con tarjetas translúcidas, efectos de desenfoque y acentos neón (#a855f7 y #38bdf8).
  - Flujo completo de Onboarding con validación de credenciales y pantalla de carga animada.
  - Dashboard central con navegación por pestañas de ancho completo, vitrina de repositorios insignia con enlaces directos a GitHub y banner Hero con avatar.
  - Chat interactivo con IA actuando como Principal Cloud & DevOps Architect con pensamiento crítico y trade-offs reales de ingeniería.

---

### 📝 Fase 4: README Studio & Optimizador Profesional de Perfil
* **🎯 Objetivo:** Generar un `README.md` de élite para GitHub que destaque la especialización en Cloud & DevOps (AWS Serverless con Terraform, Docker Labs y Linux Automation).
* **🚧 Retos / Inconvenientes:** Los modelos de IA suelen caer en clichés vacíos ("apasionado por la tecnología") y generar badges con servidores externos caídos. Se implementó un prompt estricto con pensamiento crítico y sanitización regex de encabezados para vincular números y proyectos en una sola línea.
* **✅ Lo que he logrado:**
  - Integración de Claude Sonnet 4.6 en AWS Bedrock para generación de READMEs arquitectónicos de alta fidelidad.
  - Interfaz estilo terminal con selector dual: vista previa formateada y vista de código fuente Markdown.
  - Badges fiables con `shields.io` y métricas de ingeniería de GitHub.

---

### 🎯 Fase 5: Adaptador Curricular Inteligente (TailorCV Studio & ATS Matcher)
* **🎯 Objetivo:** Auditar currículums reales frente a ofertas de empleo, identificar fallos de filtrado ATS y generar una versión optimizada ejecutable en PDF y Markdown.
* **🚧 Retos / Inconvenientes:** Los parsers ATS descartan CVs sin palabras clave normalizadas ni impacto cuantificable. Además, se resolvió la integración con `fpdf2` para generar PDFs ejecutivos en memoria y un parser XML resiliente que previene la pérdida de bloques Markdown generados por la IA.
* **✅ Lo que he logrado:**
  - Extractor de texto desde currículums en formato PDF usando `PyPDF2`.
  - Auditoría crítica con puntuación roja (25-42%) detallando los 5 errores técnicos que provocan el descarte.
  - Puntuación optimizada en verde (93-98%) con transformaciones y reescritura de viñetas bajo la **Fórmula Google X-Y-Z**.
  - Generador de PDF ejecutivo de alta resolución con tipografía TrueType y enlaces de contacto usando `fpdf2`.
  - Descarga dual del currículum en `.pdf` y `.md` con barra de progreso lineal sincronizada al 100%.

