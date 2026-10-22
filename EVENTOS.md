# Eventos y registros

La interfaz pública está en `public/eventos.php`; la administración, en `public/admin.php`. Python mantiene la API y los datos residen en MySQL/MariaDB.

## Preparación

1. Crea la base y un usuario MySQL en el hosting.
2. Importa `schema.sql` desde phpMyAdmin.
3. Configura `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` y `ADMIN_PASSWORD` como variables privadas del servicio Python.
4. Instala `requirements.txt` en el entorno virtual Python y arranca la API.
5. Configura Apache para servir `public/` y enviar `/api/` y `/uploads/` a Python en `127.0.0.1:8000`.

Los ejemplos están en `deploy/apache-vhost.conf.example` y `deploy/events-api.service.example`. No expongas el puerto Python a Internet.

## Administrar eventos

1. Abre `/admin.php` e inicia sesión.
2. Define título, descripción, fecha y hora, cupo, estado e imagen JPG/PNG/WEBP (hasta 5 MB).
3. Revisa registros y lugares disponibles, consulta asistentes, descarga el PDF o finaliza el evento.

Los asistentes se registran desde `/eventos.php`; se solicita nombre y teléfono, con correo opcional. El servidor evita teléfonos duplicados por evento y controla el cupo.

## Migrar SQLite local

Importa primero el esquema MySQL en una base destino vacía. Define `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD`, y ejecuta `python migrate_sqlite_to_mysql.py` en la carpeta que contiene `eventos.sqlite3`. El script conserva identificadores y se niega a migrar sobre datos existentes. Copia también `uploads/`. Conserva la base SQLite como respaldo hasta verificar el resultado.

Los datos de asistentes y los PDF son privados. Restringe accesos, usa HTTPS y acuerda aviso de privacidad y plazo de retención con el negocio.
