# pjecz-casiopea-api-key

API con autentificación por API-Key para comunicación con otros sistemas.

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```env
# Base de datos
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=pjecz_casiopea
DB_USER=adminpjeczcasiopea
DB_PASS=XXXXXXXXXXXXXXXX

# Origins
ORIGINS=http://localhost:3000

# Cryptography
FERNET_KEY=
SALT=

# Huso Horario
TZ=America/Mexico_City

# Control de Acceso API Key para obtener el código de acceso
CONTROL_ACCESO_URL=
CONTROL_ACCESO_API_KEY=
CONTROL_ACCESO_APLICACION=
CONTROL_ACCESO_TIMEOUT=
```
## Instalación con uv

```bash
# En desarrollo
uv sync

# En producción
uv sync --no-dev
```