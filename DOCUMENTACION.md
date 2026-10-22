# Documentación técnica y de publicación

## El Café de los Poetas Muertos

El sitio está preparado para alojarse en un servidor Linux con PHP, Python y MySQL/MariaDB. El navegador sigue recibiendo HTML: las páginas PHP generan ese contenido y pueden combinarse con CSS y JavaScript.

## Estructura

- `public/index.php`: portada, identidad del café, escritores, poemas, eventos, ubicación y redes.
- `public/menu.php`: menú de productos, ingredientes y precios.
- `public/eventos.php`: agenda pública, lugares disponibles e inscripción emergente.
- `public/admin.php`: panel de administración.
- `public/images/`: fotografías, menú e imágenes de escritores.
- `server.py`: API Python para eventos, registros y descarga PDF.
- `schema.sql`: esquema MySQL/MariaDB; se importa en la base creada por el hosting.
- `migrate_sqlite_to_mysql.py`: migración opcional de datos del SQLite local a una base destino vacía.
- `requirements.txt`: dependencia del conector MySQL para Python.
- `uploads/`: imágenes del panel; permanecen fuera del directorio público y se sirven mediante la API.
- `deploy/`: ejemplos de VirtualHost Apache y servicio systemd para la API.
- `start-server.ps1`: arranca la API en Windows y solicita configuración local.

## Arquitectura

1. Apache/PHP sirve los archivos de `public/` en el dominio.
2. Apache reenvía `/api/` y `/uploads/` a la API Python, ligada únicamente a `127.0.0.1:8000`.
3. Python valida inscripciones y administra eventos en MySQL/MariaDB.
4. phpMyAdmin se usa para mantenimiento de la base; el panel de la cafetería sigue siendo `admin.php`.

No configures la carpeta principal del proyecto como raíz del dominio; usa `public/`. Así no se exponen `server.py`, credenciales, scripts de migración ni documentación.

## Preparar la base

1. En el hosting crea una base MySQL/MariaDB y un usuario con permisos solo sobre esa base.
2. En phpMyAdmin selecciona la base recién creada e importa `schema.sql`.
3. Configura `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD` en el entorno privado del proceso Python.
4. Instala dependencias en un entorno virtual con `python -m pip install -r requirements.txt`.

No guardes contraseñas reales en el repositorio. `.env.example` documenta las variables; es una plantilla que Python no carga automáticamente.

## Migrar los datos locales

La base local `eventos.sqlite3` se mantiene como origen hasta decidir la migración. Importa primero el esquema MySQL y respalda la base destino. El script se niega a escribir si encuentra datos existentes en el destino:

```powershell
$env:DB_HOST = 'host-mysql'
$env:DB_PORT = '3306'
$env:DB_NAME = 'base_destino'
$env:DB_USER = 'usuario'
$env:DB_PASSWORD = 'clave'
python migrate_sqlite_to_mysql.py
```

Copia también `uploads/` al servidor privado para conservar las imágenes de eventos. Mantén el SQLite como respaldo hasta revisar registros e imágenes publicados. Nunca subas datos reales de asistentes a un repositorio público.

## Publicación en VPS

El directorio del dominio debe apuntar a `public/`. Instala Apache con PHP-FPM, Python 3, MySQL/MariaDB y módulos proxy de Apache. Usa `deploy/apache-vhost.conf.example` como base y reemplaza dominio, rutas y socket PHP-FPM según la distribución. Activa el certificado HTTPS y redirección HTTP a HTTPS antes de usar cookies seguras.

Instala la API como servicio persistente siguiendo `deploy/events-api.service.example`. Coloca sus variables en `/etc/elcafe/events.env` con permisos restringidos; ajusta rutas/usuario y permite a la cuenta de servicio escribir únicamente en `uploads/`. Mantén el puerto 8000 cerrado al exterior. Configura firewall, actualizaciones, copias de seguridad de MySQL y `uploads/`, y monitoreo de errores.

Las páginas usan el mismo dominio para consumir `/api/` y `/uploads/`, rutas que Apache reenvía a Python. El JavaScript depende de que se conserven esas rutas.

### Alojamiento compatible

Se necesita un VPS o alojamiento que permita mantener PHP y un proceso Python persistente. Por ejemplo, Hostinger indica que Python se admite en sus VPS; sus planes Web/Cloud ofrecen PHP y MySQL/MariaDB con phpMyAdmin, pero no Python. Si se elige ese proveedor, hace falta un VPS y configurar el stack. [Compatibilidad Python de Hostinger](https://support.hostinger.com/en/articles/3648030-is-python-supported-at-hostinger) · [Bases de datos compatibles](https://www.hostinger.com/support/which-databases-and-data-tools-are-supported-at-hostinger/).

El dominio, cuenta de hosting, certificado, costo, responsable de mantenimiento y acceso DNS todavía deben definirse. El proyecto no está publicado ni se ha comprado ningún servicio.

## Gestión de eventos

En `https://dominio/admin.php` iniciar sesión con `ADMIN_PASSWORD`, definida al arrancar el servicio. Crear o editar eventos con título, descripción, fecha, hora, cupo, estado e imagen JPG/PNG/WEBP (hasta 5 MB). El panel permite cambiar el estado, consultar asistentes, descargar el PDF y eliminar eventos.

El público se registra en `https://dominio/eventos.php`. Nombre y teléfono son obligatorios; el correo es opcional. Python aplica el límite de cupo, cierra eventos vencidos y evita teléfonos duplicados dentro de cada evento. La tarjeta muestra registros y lugares libres.

## API

- `GET /api/events`: eventos con `registered` y `available`.
- `POST /api/events/register`: registra una persona.
- `POST /api/login` y `POST /api/logout`: sesión administrativa.
- `GET /api/admin/events`: lista eventos (requiere sesión).
- `POST /api/admin/events`: crea evento.
- `PUT /api/admin/events/{id}`: actualiza evento.
- `DELETE /api/admin/events/{id}`: elimina evento y asistentes asociados.
- `GET /api/admin/events/{id}/registrations`: lista privada de asistentes.
- `GET /api/admin/events/{id}/registrations.pdf`: PDF privado de asistentes.
- `GET /api/health`: diagnóstico básico.

En producción configura `COOKIE_SECURE=1` después de habilitar HTTPS.

## Protección de datos

Nombres, teléfonos y correos son datos personales. Restringe la cuenta SQL, phpMyAdmin, el panel y los PDFs; usa HTTPS; acuerda aviso de privacidad y plazo de retención; habilita respaldos protegidos y procedimiento de eliminación.

## Documentos

- `EVENTOS.md`: resumen operativo.
- `documentacion/PROPUESTA_CLIENTE.pdf`: propuesta de migración PHP + Python + MySQL y publicación.
- `documentacion/PROPUESTA_CLIENTE.html`: fuente editable del PDF.
