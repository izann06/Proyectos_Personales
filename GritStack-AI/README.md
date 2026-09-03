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

## 🚀 Próximos Pasos (Lo que estoy haciendo ahora)
1. **Fase 0**: Configurando la arquitectura y las herramientas básicas.
2. **Fase 1**: Conectaré la API de GitHub para que la aplicación empiece a "leer" repositorios.
