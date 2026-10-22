# El café de los poetas muertos

Sitio web y sistema de eventos de la cafetería. Usa PHP para las páginas, Python para la API y MySQL para guardar eventos e inscripciones.

## Demo en GitHub Pages

La carpeta `docs/` contiene una versión estática de la portada, el menú visual y la página informativa de eventos. Se genera con:

**Sitio publicado:** https://doozerdragon.github.io/cafe-poetas-muertos-web/

```powershell
.\build-pages.ps1
```

GitHub Pages debe publicarse desde la rama principal y la carpeta `/docs`. La agenda con inscripciones y el panel administrativo requieren el servidor Python y MySQL descritos más abajo, por lo que la demo estática muestra un aviso informativo en esa sección.

## Archivos principales

- `public/`: páginas PHP e imágenes públicas.
- `server.py`: API de eventos, registros, administración y exportación PDF.
- `schema.sql`: tablas MySQL.
- `requirements.txt`: dependencias Python.
- `start-server.ps1`: inicia la API en Windows y solicita la configuración privada.
- `migrate_sqlite_to_mysql.py`: migración opcional desde la base SQLite local.
- `deploy/`: ejemplos de configuración para Apache y systemd.
- `DOCUMENTACION.md` y `EVENTOS.md`: despliegue y operación.

## Ejecutar localmente con XAMPP en Windows

1. Inicia **MySQL** desde el panel de XAMPP. Crea la base `el_cafe_poetas_muertos` e importa `schema.sql` desde phpMyAdmin si aún no existe.
2. Instala las dependencias de Python una vez:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Abre una terminal en la carpeta del proyecto y sirve PHP en el puerto `8080`:

   ```powershell
   C:\xampp\php\php.exe -S 127.0.0.1:8080 -t public
   ```

4. En otra terminal, ejecuta `.\start-server.ps1`. El script solicita una clave de administrador y los datos de MySQL. En una instalación XAMPP local suelen ser host `127.0.0.1`, puerto `3306`, base `el_cafe_poetas_muertos`, usuario `root` y contraseña vacía.
5. Abre [http://127.0.0.1:8080/](http://127.0.0.1:8080/). La API Python escucha en `127.0.0.1:8000`; mantén abiertas ambas terminales.

En desarrollo local, las páginas PHP se conectan a la API de `127.0.0.1:8000`. En producción, Apache debe servir `public/` y reenviar `/api/` y `/uploads/` a la API, como muestra `deploy/apache-vhost.conf.example`.

## Configuración de producción

Instala PHP con PDO MySQL, Python 3, MySQL/MariaDB y Apache. Configura `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` y `ADMIN_PASSWORD` como variables privadas del proceso Python. `.env.example` enumera las variables; Python no carga ese archivo automáticamente. Consulta `DOCUMENTACION.md` y `EVENTOS.md` antes de publicar.

La base SQLite local, los registros, las credenciales, los logs y el contenido de `uploads/` se excluyen de Git. Conserva SQLite como respaldo privado hasta verificar cualquier migración.

## Trabajo en equipo

Cada persona debe crear una rama para sus cambios y abrir un pull request hacia `main`. No compartan contraseñas por Git; configura valores locales propios.
