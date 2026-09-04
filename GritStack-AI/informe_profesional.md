# Informe de Análisis de Talento Tecnológico — `izann06`

---

## 1. RESUMEN PROFESIONAL

Izan es un desarrollador de 20 años con formación en el ciclo superior de Desarrollo de Aplicaciones Multiplataforma (DAM), actualmente en una etapa de transición activa hacia el mundo **Cloud y DevOps**. Su perfil es el de un **junior con una curiosidad técnica notable y una capacidad de autoaprendizaje estructurada**: documenta su progreso de forma metódica, construye laboratorios prácticos propios y trabaja con tecnologías de nivel profesional (Terraform, Docker, AWS, CI/CD) de forma autodidacta, más allá de lo exigido en sus estudios. Paralelamente, mantiene experiencia laboral en un entorno corporativo (SAP/Cuentas por Pagar), lo que le aporta una visión de negocio poco común en perfiles de su edad. Su stack académico es sólido en C#, Kotlin y Java, mientras que su stack personal apunta claramente hacia infraestructura cloud, automatización y contenedores.

---

## 2. HABILIDADES TÉCNICAS CONFIRMADAS

### 🖥️ Lenguajes de Programación
| Tecnología | Evidencia | Nivel estimado |
|---|---|---|
| **C#** | ~2.57 MB de código (1DAM + 2DAM + Monopoly) | Intermedio-Alto |
| **Kotlin** | ~576 KB (2DAM, Android con Jetpack Compose, Room, Retrofit) | Intermedio |
| **Java** | ~563 KB (1DAM + 2DAM + NewGarage) | Intermedio |
| **Python** | ~153 KB (proyectos personales, Lambda AWS, FastAPI, boto3) | Intermedio |
| **TypeScript** | ~949 KB (Monopoly frontend con React) | Intermedio |
| **JavaScript** | ~85 KB (varios proyectos) | Básico-Intermedio |
| **HTML/CSS** | ~272 KB combinados | Básico-Intermedio |
| **PHP** | ~133 KB (1DAM) | Básico |
| **Shell/Bash** | Proyectos DevOps | Básico |

### 🧩 Frameworks y Librerías
- **ASP.NET Core** — Backend del proyecto Monopoly (API REST + SignalR)
- **React + TypeScript** — Frontend del proyecto Monopoly (con TailwindCSS, Vite)
- **FastAPI** — APIs REST en Python dentro de Docker Labs
- **Express.js** — APIs Node.js en Docker Labs
- **Jetpack Compose** — UI declarativa Android (documentado en apuntes)
- **Room / Retrofit / LiveData** — Persistencia y red en Android
- **LibGDX + Box2D** — Desarrollo de videojuegos 2D (documentado)
- **CustomTkinter** — GUI de escritorio en Python (Dark Passenger Backup)

### 🗄️ Bases de Datos
- **MySQL** — Usado en Docker Labs y proyecto Monopoly
- **PostgreSQL** — Usado en Docker Labs (con pgAdmin)
- **Redis** — Caché en stack JWT de Docker Labs
- **Entity Framework Core** — ORM en proyecto Monopoly (MySQL + InMemory)
- **Room (SQLite)** — Persistencia local Android
- **PL/SQL** — Básico (1DAM)

### ☁️ DevOps / Cloud / Infraestructura
- **Docker & Docker Compose** — Laboratorio progresivo de 6 proyectos documentados, multicontenedor
- **Terraform (HCL)** — IaC para arquitectura AWS Serverless (~11 KB de código real)
- **AWS** — Lambda, S3, Polly, IAM, EC2, RDS, DynamoDB, VPC, Bedrock, Amazon Q (conocimiento teórico-práctico)
- **GitHub Actions** — CI/CD para despliegue automático (Quartz/GitHub Pages, workflow de deployment)
- **Linux** — Administración básica, SSH, Nginx, rsync (proyectos DevOps RoadMap)
- **Vagrant** — Virtualización (documentado en apuntes)
- **Nginx** — Servidor web estático (proyecto DevOps)

### 🛠️ Herramientas y Otros
- **Git / GitHub** — Control de versiones, ramas, gitignore, flujos de trabajo
- **Obsidian + Quartz** — Gestión de conocimiento personal con publicación web automatizada
- **SignalR** — WebSockets en tiempo real (Monopoly)
- **JWT + Bcrypt** — Autenticación segura (Docker Labs)
- **n8n / Portainer / Homepage** — Stack homelab DevOps
- **SAP** — Experiencia laboral en entorno corporativo (Cuentas por Pagar)

---

## 3. PROYECTOS DESTACADOS

### 🥇 1. Monopoly Online Multijugador (Proyecto de fin de ciclo DAM)
**Repositorio:** `Raul1156/monopoly` (colaboración)

**Por qué destaca:** Es el proyecto técnicamente más complejo del perfil. Implementa una arquitectura **full-stack completa y real**: backend en ASP.NET Core con API REST + WebSockets (SignalR), frontend en React/TypeScript, base de datos MySQL en Docker, y **despliegue real en AWS**. La separación en capas (Controllers, Services, Repositories, DTOs), la gestión de estado efímero en memoria para partidas activas y la sincronización en tiempo real entre múltiples jugadores demuestran comprensión de conceptos de ingeniería de software que van más allá del nivel esperado en un ciclo formativo. El hecho de que esté desplegado y accesible públicamente es un diferenciador importante.

---

### 🥈 2. Docker Labs
**Repositorio:** `izann06/Docker-Labs`

**Por qué destaca:** Demuestra una **metodología de aprendizaje estructurada y progresiva** que imita el trabajo real de un DevOps engineer. El laboratorio escala desde un Dockerfile básico hasta un homelab con Zero-Trust networking, healthchecks, autenticación JWT con Redis, y un stack de automatización con n8n y Portainer. La documentación es clara, profesional y con tablas de referencia de puertos. No es un tutorial copiado: hay decisiones de arquitectura propias y resolución de problemas reales documentados.

---

### 🥉 3. AWS Serverless Text-to-Speech
**Repositorio:** `izann06/aws-serverless-text-to-speech`

**Por qué destaca:** Es un proyecto pequeño pero **muy revelador del nivel de madurez técnica** del desarrollador. Combina Terraform (IaC), AWS Lambda (Python/boto3), S3, Polly e IAM en una arquitectura event-driven real. Lo más valioso no es el código en sí, sino la documentación de los errores cometidos y sus soluciones (AccessDenied por IAM, MalformedPolicyDocument, gestión del tfstate), lo que evidencia que ha trabajado de verdad con las herramientas y no solo ha seguido un tutorial. Mantener la factura en 0€ usando el free tier también demuestra criterio económico.

---

## 4. ÁREAS DE MEJORA

### Brechas técnicas prioritarias
- **Testing:** No hay ninguna evidencia de tests unitarios, de integración o E2E en ningún repositorio (JUnit, pytest, xUnit, Cypress...). Es una carencia crítica para cualquier entorno profesional.
- **Kubernetes:** Docker está cubierto, pero K8s es el siguiente paso natural en el roadmap Cloud/DevOps y no aparece en ningún proyecto.
- **Observabilidad:** No hay evidencia de uso de herramientas de monitorización real (Prometheus, Grafana, CloudWatch en profundidad, Datadog). Fundamental en roles DevOps/SRE.
- **Seguridad aplicada (AppSec):** Los apuntes mencionan conceptos de seguridad, pero no hay proyectos que implementen prácticas de seguridad en el código (SAST, gestión de secretos con Vault/AWS Secrets Manager, análisis de vulnerabilidades en contenedores).
- **CI/CD avanzado:** Los pipelines existentes son básicos (despliegue estático). Falta experiencia con pipelines complejos: build, test, lint, security scan, deploy con rollback.

### Brechas de visibilidad y portfolio
- **Proyectos propios con impacto medible:** La mayoría de repositorios son laboratorios de aprendizaje o trabajos académicos. Falta un proyecto personal end-to-end con usuarios reales o métricas de uso.
- **Contribuciones open source:** No hay evidencia de contribuciones a proyectos externos, lo que limita la visibilidad en la comunidad.
- **Certificaciones formales:** El conocimiento de AWS está documentado pero no hay mención de certificaciones oficiales (AWS Cloud Practitioner sería el paso inmediato y coherente con su nivel actual).

---

## 5. PUESTOS DE TRABAJO RECOMENDADOS

### 🎯 1. Junior Cloud/DevOps Engineer
**Encaje:** Alto. Es el puesto más alineado con su trayectoria autodidacta reciente. Domina Docker, Terraform, GitHub Actions, Linux básico y AWS a nivel práctico. Su capacidad de documentar y estructurar entornos complejos es un activo real. Empresas con cultura de aprendizaje interno (startups, consultoras tecnológicas) serían el entorno ideal para consolidar este perfil.

**Gap a cubrir antes:** Kubernetes básico y alguna certificación AWS.

---

### 🎯 2. Junior Backend Developer (.NET / Java / Kotlin)
**Encaje:** Alto. Tiene la base académica más sólida en C# y Java, con un proyecto real de ASP.NET Core en producción (Monopoly con SignalR, EF Core, arquitectura en capas). El conocimiento de Android con Kotlin y arquitecturas modernas (MVVM, Room, Retrofit) abre también la puerta al desarrollo móvil nativo.

**Gap a cubrir antes:** Testing automatizado y experiencia con patrones de diseño más avanzados.

---

### 🎯 3. Junior Platform / Infrastructure Engineer (Interno)
**Encaje:** Medio-Alto. Su experiencia laboral actual en un entorno corporativo con SAP, combinada con sus conocimientos de automatización, scripting y Cloud, lo posicionan bien para roles internos en empresas medianas/grandes que buscan perfiles que entiendan tanto el negocio como la infraestructura. Roles como "IT Operations Junior", "Systems Administrator Jr." o "Platform Engineer Trainee" serían una transición natural desde su posición actual.

**Gap a cubrir antes:** Profundizar en redes, seguridad corporativa y herramientas de ITSM.

---

*Informe generado a partir de evidencia directa del perfil público de GitHub. Las estimaciones de nivel son relativas al mercado laboral junior/mid español (2025).*