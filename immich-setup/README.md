# 🖼️ Immich + Dark Passenger Backup

## ¿Qué es Immich?

**Immich** es tu propio Google Photos, pero funcionando en tu ordenador. Las fotos y vídeos de tu móvil se envían por WiFi a tu PC y se guardan ahí, sin pasar por ninguna nube de terceros. Tú tienes el control total.

Y lo mejor: tiene reconocimiento facial, búsqueda inteligente, álbumes compartidos y una app de móvil que funciona genial. Es como tener Google Photos pero sin pagar y sin que nadie vea tus fotos.

## ¿Cómo encaja con Dark Passenger?

La idea es sencilla. Son dos piezas que encajan juntas:

```
📱 Tu móvil
   │
   │  (WiFi, automático)
   ▼
💻 Tu PC con Immich
   │  Las fotos se guardan en E:\DarkPassenger_Backup\Immich
   │
   │  (Cuando conectas el SSD)
   ▼
💾 Tu SSD externo con Dark Passenger Backup
   Las fotos se copian de forma segura al disco externo
```

- **Immich** se encarga de recoger las fotos del móvil y guardarlas en tu PC.
- **Dark Passenger** se encarga de copiar esa carpeta al SSD cuando lo conectes.

No se hablan entre ellas. No hace falta. Immich deja las fotos en una carpeta, y Dark Passenger copia esa carpeta. Así de simple.

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

### Paso 5 — Conecta con Dark Passenger Backup

Ahora solo falta decirle a Dark Passenger que proteja esa carpeta:

1. Abre **Dark Passenger Backup**.
2. Ve a **📁 Carpetas**.
3. Pulsa **"+ Añadir Carpeta"**.
4. Selecciona la carpeta `E:\DarkPassenger_Backup\Immich`.
5. Hecho. La próxima vez que conectes el SSD, tus fotos del móvil también se copiarán.

---

## 🧠 Preguntas frecuentes

### ¿Necesito tener el PC encendido para que funcione?
Sí. Immich es un servidor que corre en tu PC. Si el PC está apagado, las fotos se quedan en el móvil esperando. En cuanto enciendas el PC, la app del móvil las enviará automáticamente.

### ¿Se borran las fotos de mi móvil?
No, a menos que tú lo hagas manualmente. Immich solo copia, no borra nada del móvil.

### ¿Qué pasa si reinstalo Immich?
Mientras no borres la carpeta `E:\DarkPassenger_Backup\Immich`, tus fotos siguen ahí. La base de datos (álbumes, caras, etc.) se guarda en un volumen de Docker que también persiste.

### ¿Puedo acceder desde fuera de casa?
Sí, pero requiere configuración extra (un túnel o abrir puertos en el router). Por defecto solo funciona dentro de tu red WiFi local, que es lo más seguro.

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
