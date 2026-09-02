# 🖼️ Immich + Dark Passenger Backup

## ¿Qué es Immich?

**Immich** es tu propio Google Photos, pero funcionando en tu ordenador. Las fotos y vídeos de tu móvil se envían por WiFi a tu PC y se guardan ahí, sin pasar por ninguna nube de terceros. Tú tienes el control total.

Y lo mejor: tiene reconocimiento facial, búsqueda inteligente, álbumes compartidos y una app de móvil que funciona genial. Es como tener Google Photos pero sin pagar y sin que nadie vea tus fotos.

## ¿Cómo encaja con Dark Passenger?

La idea es sencilla. Son dos piezas que encajan juntas:

```text
📱 Tu móvil                  💻 Tu PC (Documentos, Código...)
   │                               │
   │ (Vía WiFi)                    │ (Vía Dark Passenger App)
   ▼                               ▼
   └───────────► 💾 Tu SSD Externo ◄───────────┘
            Las dos vías conviven en el mismo disco
```

- **Immich** se encarga de recoger las fotos del móvil en tiempo real y guardarlas directamente en el SSD (`E:\`).
- **Dark Passenger** se encarga de tus documentos, código y archivos importantes del PC, respaldándolos en el SSD.

Ambas herramientas forman tu ecosistema de copias de seguridad completo y definitivo.

---

## 🚀 Instalación paso a paso

### Requisito: Docker Desktop

Immich funciona con Docker. Si no lo tienes instalado:

1. Ve a [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) y descárgalo.
2. Instálalo (siguiente, siguiente, siguiente...).
3. Ábrelo una vez para que termine de configurarse.
4. Déjalo abierto en segundo plano (se queda en la bandeja del sistema, como Dark Passenger).

### Paso 1 — Revisa la configuración

Abre el archivo `.env.example` que está en esta misma carpeta. Verás esto:

```
UPLOAD_LOCATION=C:\
DB_PASSWORD=postgres
```

- **UPLOAD_LOCATION**: Es la carpeta donde se van a guardar todas tus fotos. Está configurada para que vayan directamente a la ruta que pongas, así Dark Passenger ya tiene acceso a ellas cuando hagas backup.
- **DB_PASSWORD**: Cámbiala por algo más seguro si quieres (no necesitas recordarla).

### Paso 2 — Arranca Immich

Abre PowerShell o una terminal dentro de esta carpeta (`immich-setup`) y ejecuta:

```bash
docker compose up -d
```

La primera vez tardará unos minutos en descargar todo. Verás algo así:

```
✔ Container immich_redis        Started
✔ Container immich_postgres     Started
✔ Container immich_server       Started
✔ Container immich_machine_learning  Started
```

### Paso 3 — Entra en Immich

Abre tu navegador y ve a:

```
http://localhost:2283
```

Te pedirá crear una cuenta de administrador. Ponle tu nombre, email y una contraseña (esto es solo local, no se envía a ningún sitio).

### Paso 4 — Instala la app en tu móvil

1. Descarga **Immich** en tu móvil (está en [Google Play](https://play.google.com/store/apps/details?id=app.alextran.immich) y en [App Store](https://apps.apple.com/app/immich/id1613945686)).
2. Abre la app y en la URL del servidor pon la IP local de tu PC con el puerto. Por ejemplo: `http://192.168.1.50:2283` (tu IP puede ser diferente, la puedes encontrar abriendo una terminal y escribiendo `ipconfig`).
3. Inicia sesión con la cuenta que acabas de crear.
4. Activa la copia de seguridad automática en la app.
5. ¡Listo! Tus fotos empezarán a enviarse automáticamente.

### ⚠️ IMPORTANTE: Si la app del móvil no logra conectar (Problema del Firewall)

A veces, al poner la IP en el móvil, la app se queda cargando y da error. **Esto es completamente normal en Windows.**

**¿Por qué ocurre?**
Windows tiene un "escudo" (el Firewall) que bloquea por defecto cualquier conexión entrante a tu PC para protegerlo. Aunque Immich esté funcionando perfectamente por dentro, el Firewall detiene la petición del móvil antes de que llegue a Immich.

**¿Cómo se soluciona?**
Hay que decirle a Windows que abra una "puerta" específica (el puerto 2283) para dejar pasar a tu móvil.

1. Presiona la tecla **Windows**, escribe `PowerShell`.
2. A la derecha, pulsa en **Ejecutar como administrador** (dile que Sí a la ventanita).
3. Pega este comando y dale a Enter:
   ```powershell
   New-NetFirewallRule -DisplayName "Immich Port 2283" -Direction Inbound -LocalPort 2283 -Protocol TCP -Action Allow
   ```
4. En cuanto le des a Enter, el muro caerá. Vuelve a probar en tu móvil y verás que conecta al instante.

### Paso 5 — ¿Para qué sirve Dark Passenger entonces?

Como has configurado Immich para que guarde las fotos **directamente en tu SSD** (`E:\`), Dark Passenger ya no necesita copiar esas fotos (porque ya están ahí físicamente).

Entonces, ¿para qué sirve tener tu aplicación Dark Passenger y este repositorio de Immich juntos? Porque forman el ecosistema de seguridad perfecto con dos vías independientes:

1. **La Vía del Móvil (Immich):** Se encarga **en exclusiva** de tus fotos. Coge las fotos de tu móvil por WiFi y las mete directamente en tu SSD externo de forma ordenada.
2. **La Vía del PC (Dark Passenger):** Se encarga del resto de tu vida digital. Documentos del ordenador, facturas, apuntes, proyectos de programación y carpetas del sistema. Dark Passenger coge todo eso de tu PC y lo respalda de forma segura en tu SSD.

Ambos sistemas conviven juntos en tu disco duro para darte una copia de seguridad total de tu vida digital.

---

## 🧠 Preguntas frecuentes

### ¿Necesito tener el PC encendido para que funcione?
Sí. Immich es un servidor que corre en tu PC. Si el PC está apagado, las fotos se quedan en el móvil esperando. En cuanto enciendas el PC, la app del móvil las enviará automáticamente.

**¿Tengo que abrir Docker y poner `docker compose up -d` cada vez que enciendo el ordenador?**
¡No! Está configurado con la instrucción `restart: always`. Esto significa que si Docker Desktop se abre al iniciar Windows, tus contenedores arrancarán mágicamente en segundo plano sin que tú toques nada.

**Para asegurarte de que Docker arranca con tu PC:**
1. Abre **Docker Desktop** en tu ordenador.
2. Haz clic en la **Rueda de engranaje (Ajustes)** arriba a la derecha.
3. En la pestaña **General**, marca la casilla que dice: *"Start Docker Desktop when you log in"*.
4. Dale a **Apply & restart** abajo a la derecha. ¡Ya está! Nunca más tendrás que acordarte de abrirlo.

### ¿Se borran las fotos de mi móvil?
No, a menos que tú lo hagas manualmente. Immich solo copia, no borra nada del móvil.

### Si se me rompe el SSD pero tengo el volumen de Docker... ¿salvo mis fotos?
**NO.** Mucho cuidado con esto: el "volumen de Docker" (la base de datos) solo guarda *los metadatos* (nombres de los álbumes, las caras reconocidas, tus contraseñas, etc.). **Las fotos y vídeos físicos reales** se guardan en la carpeta `UPLOAD_LOCATION` (es decir, dentro de tu SSD).
- Si se rompe el PC pero el SSD sobrevive: Estás a salvo. Tienes las fotos en el SSD.
- Si se rompe el SSD: **Pierdes las fotos**. Por eso los profesionales siempre tienen *dos* copias físicas de las cosas importantes.

### ¿Puedo acceder desde fuera de casa (con 4G o en la calle)?
Por defecto, no. Immich solo funciona cuando tu móvil está conectado al mismo WiFi que el ordenador, que es lo más seguro y privado. 
Sin embargo, **sí es posible hacerlo** si configuras una red virtual segura (como **Tailscale** o **Cloudflare Tunnels**). Son herramientas gratuitas que instalan un "túnel" privado entre tu móvil y tu PC estés donde estés, sin necesidad de abrir puertos peligrosos en el router de tu casa.

---

## 🛑 Comandos útiles

| Qué quieres hacer | Comando |
|:---|:---|
| Arrancar Immich | `docker compose up -d` |
| Parar Immich | `docker compose down` |
| Ver qué está pasando (logs) | `docker compose logs -f` |
| Actualizar a la última versión | `docker compose pull && docker compose up -d` |
| Ver si los contenedores están corriendo | `docker compose ps` |

> Todos estos comandos se ejecutan desde esta carpeta (`immich-setup`).
