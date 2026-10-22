"""Backend local para eventos, registros y administración del Café."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import mimetypes
import os
import re
import secrets
import time
from datetime import datetime
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import mysql.connector
from mysql.connector import IntegrityError

mimetypes.add_type("image/webp", ".webp")

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / "uploads"
MAX_BODY = 7 * 1024 * 1024
MAX_IMAGE = 5 * 1024 * 1024
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_NAME = os.environ.get("DB_NAME", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "0") == "1"
SESSION_KEY = secrets.token_bytes(32)
SESSIONS: dict[str, float] = {}
LOGIN_ATTEMPTS: dict[str, list[float]] = {}

if len(ADMIN_PASSWORD) < 12:
    raise SystemExit("Configura ADMIN_PASSWORD con al menos 12 caracteres antes de iniciar el servidor.")


class MySQLDatabase:
    """Pequeño adaptador para ejecutar consultas y confirmar transacciones."""

    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, charset="utf8mb4", connection_timeout=15,
            autocommit=False,
        )

    def __enter__(self) -> "MySQLDatabase":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self.connection.close()

    def execute(self, statement: str, parameters: tuple = ()):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(statement, parameters)
        return cursor

    def begin(self) -> None:
        self.connection.start_transaction()


def connect_db() -> MySQLDatabase:
    return MySQLDatabase()


def initialize_db() -> None:
    if not DB_NAME or not DB_USER:
        raise SystemExit("Configura DB_NAME y DB_USER antes de iniciar el servidor.")
    UPLOAD_DIR.mkdir(exist_ok=True)
    with connect_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS events (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(120) NOT NULL,
          description TEXT NOT NULL,
          starts_at DATETIME NOT NULL,
          capacity INT UNSIGNED NOT NULL,
          image VARCHAR(255) NULL,
          status VARCHAR(16) NOT NULL DEFAULT 'active',
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          INDEX events_status_date_idx (status, starts_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        db.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
          event_id BIGINT UNSIGNED NOT NULL,
          name VARCHAR(100) NOT NULL,
          phone VARCHAR(30) NOT NULL,
          email VARCHAR(160) NOT NULL DEFAULT '',
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          UNIQUE KEY registration_event_phone_uq (event_id, phone),
          CONSTRAINT registrations_event_fk FOREIGN KEY (event_id)
            REFERENCES events(id) ON DELETE CASCADE,
          INDEX registrations_event_idx (event_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)


def json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False).encode("utf-8")


def clean_text(value: object, limit: int) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())[:limit]


def image_from_data_url(value: object) -> str | None:
    if not value:
        return None
    if not isinstance(value, str) or len(value) > (MAX_IMAGE * 4 // 3 + 100):
        raise ValueError("La imagen no debe superar 5 MB.")
    match = re.fullmatch(r"data:(image/(?:jpeg|png|webp));base64,([A-Za-z0-9+/=]+)", value)
    if not match:
        raise ValueError("Sube una imagen JPG, PNG o WEBP.")
    raw = base64.b64decode(match.group(2), validate=True)
    if len(raw) > MAX_IMAGE:
        raise ValueError("La imagen no debe superar 5 MB.")
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[match.group(1)]
    filename = secrets.token_hex(16) + ext
    (UPLOAD_DIR / filename).write_bytes(raw)
    return "/uploads/" + filename


def event_row(db: MySQLDatabase, row: dict) -> dict:
    registered = db.execute("SELECT COUNT(*) AS total FROM registrations WHERE event_id=%s", (row["id"],)).fetchone()["total"]
    starts_at = row["starts_at"]
    starts_at = starts_at.strftime("%Y-%m-%dT%H:%M") if hasattr(starts_at, "strftime") else str(starts_at).replace(" ", "T")[:16]
    return {"id": row["id"], "name": row["name"], "description": row["description"],
            "startsAt": starts_at, "capacity": row["capacity"], "registered": registered,
            "available": max(0, row["capacity"] - registered), "image": row["image"], "status": row["status"]}


def pdf_escape(text: str) -> bytes:
    encoded = text.encode("cp1252", errors="replace")
    return encoded.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def registrations_pdf(event: dict, people: list[dict]) -> bytes:
    pages: list[list[str]] = []
    lines = ["Registro de asistentes", event["name"], "Fecha y hora: " + event["startsAt"],
             f"Cupo: {event['capacity']}   Inscritos: {len(people)}", "", "No.   Nombre                         Telefono                   Correo"]
    for i, person in enumerate(people, 1):
        line = f"{i:<5} {person['name'][:29]:<30} {person['phone'][:23]:<24} {person['email'][:38]}"
        lines.append(line)
    for start in range(0, len(lines), 42):
        pages.append(lines[start:start + 42])
    if not pages:
        pages = [[]]
    objects: list[bytes] = []
    page_ids = [4 + i * 2 for i in range(len(pages))]
    content_ids = [i + 1 for i in page_ids]
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = b" ".join(f"{i} 0 R".encode() for i in page_ids)
    objects.append(b"<< /Type /Pages /Kids [" + kids + f"] /Count {len(pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for page_id, content_id, page_lines in zip(page_ids, content_ids, pages):
        commands = [b"BT", b"/F1 10 Tf", b"50 790 Td", b"14 TL"]
        for line in page_lines:
            commands.extend([b"(" + pdf_escape(line) + b") Tj", b"T*"])
        commands.append(b"ET")
        stream = b"\n".join(commands)
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>".encode())
        objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    return bytes(output)


class Handler(BaseHTTPRequestHandler):
    server_version = "CafeEvents/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} {fmt % args}")

    def respond(self, status: int, body: bytes = b"", content_type: str = "application/json; charset=utf-8",
                headers: dict[str, str] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Cache-Control", "no-store" if self.path.startswith("/api/") else "no-cache")
        origin = self.headers.get("Origin", "")
        parsed_origin = urlparse(origin)
        local_ports = {None, 80, 3000, 5173, 5500, 5501, 8000, 8080}
        local_preview = (parsed_origin.scheme == "http" and parsed_origin.hostname in {"localhost", "127.0.0.1"}
                         and parsed_origin.port in local_ports)
        if local_preview:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            self.send_header("Vary", "Origin")
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def send_json(self, status: int, value: object, headers: dict[str, str] | None = None) -> None:
        self.respond(status, json_bytes(value), headers=headers)

    def public_preview_headers(self) -> dict[str, str]:
        """Permite que la vista previa local lea la lista pública de eventos."""
        origin = self.headers.get("Origin", "")
        if origin == "null":
            return {"Access-Control-Allow-Origin": origin, "Vary": "Origin"}
        return {}

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length > MAX_BODY:
            raise ValueError("La solicitud supera el tamaño permitido.")
        payload = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(payload, dict):
            raise ValueError("Solicitud no válida.")
        return payload

    def session_id(self) -> str | None:
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        morsel = cookie.get("cafe_admin")
        if not morsel:
            return None
        token = morsel.value
        sid, sep, signature = token.partition(".")
        expected = hmac.new(SESSION_KEY, sid.encode(), hashlib.sha256).hexdigest()
        if not sep or not hmac.compare_digest(signature, expected):
            return None
        if SESSIONS.get(sid, 0) < time.time():
            SESSIONS.pop(sid, None)
            return None
        SESSIONS[sid] = time.time() + 8 * 60 * 60
        return sid

    def require_admin(self) -> bool:
        if self.session_id():
            return True
        self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "Inicia sesión como administrador."})
        return False

    def check_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        parsed = urlparse(origin)
        if parsed.netloc == self.headers.get("Host"):
            return True
        local_ports = {None, 80, 3000, 5173, 5500, 5501, 8000, 8080}
        if (parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1"}
                and parsed.port in local_ports):
            return True
        self.send_json(HTTPStatus.FORBIDDEN, {"error": "Origen no permitido."})
        return False

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path == "/api/events":
            now = datetime.now().replace(second=0, microsecond=0)
            with connect_db() as db:
                db.execute("UPDATE events SET status='finished' WHERE status='active' AND starts_at<=%s", (now,))
                rows = db.execute("SELECT * FROM events ORDER BY starts_at ASC").fetchall()
                events = [event_row(db, row) for row in rows]
            self.send_json(200, {"events": events}, self.public_preview_headers())
            return
        if path == "/api/admin/events":
            if not self.require_admin(): return
            with connect_db() as db:
                rows = db.execute("SELECT * FROM events ORDER BY starts_at DESC").fetchall()
                self.send_json(200, {"events": [event_row(db, row) for row in rows]})
            return
        match = re.fullmatch(r"/api/admin/events/(\d+)/registrations\.pdf", path)
        if match:
            if not self.require_admin(): return
            event_id = int(match.group(1))
            with connect_db() as db:
                row = db.execute("SELECT * FROM events WHERE id=%s", (event_id,)).fetchone()
                if not row:
                    self.send_json(404, {"error": "Evento no encontrado."}); return
                event = event_row(db, row)
                people = db.execute("SELECT name,phone,email FROM registrations WHERE event_id=%s ORDER BY created_at,id", (event_id,)).fetchall()
            filename = re.sub(r"[^a-zA-Z0-9_-]+", "-", event["name"]).strip("-") or "evento"
            self.respond(200, registrations_pdf(event, people), "application/pdf",
                         {"Content-Disposition": f'attachment; filename="registros-{filename}.pdf"'})
            return
        match = re.fullmatch(r"/api/admin/events/(\d+)/registrations", path)
        if match:
            if not self.require_admin(): return
            with connect_db() as db:
                exists = db.execute("SELECT id FROM events WHERE id=%s", (int(match.group(1)),)).fetchone()
                if not exists:
                    self.send_json(404, {"error": "Evento no encontrado."}); return
                people = db.execute("SELECT id,name,phone,email,created_at FROM registrations WHERE event_id=%s ORDER BY created_at,id", (int(match.group(1)),)).fetchall()
                registrations = [{**person, "created_at": person["created_at"].isoformat(sep=" ", timespec="seconds")}
                                 for person in people]
                self.send_json(200, {"registrations": registrations})
            return
        if path.startswith("/uploads/"):
            filename = Path(path).name
            file_path = UPLOAD_DIR / filename
            if file_path.is_file() and file_path.parent == UPLOAD_DIR:
                self.respond(200, file_path.read_bytes(), mimetypes.guess_type(file_path.name)[0] or "application/octet-stream")
            else:
                self.send_json(404, {"error": "Imagen no encontrada."})
            return
        if path == "/api/health":
            self.send_json(200, {"ok": True}); return
        self.respond(404, b"Not found", "text/plain; charset=utf-8")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/login":
            remote = self.client_address[0]
            recent = [stamp for stamp in LOGIN_ATTEMPTS.get(remote, []) if stamp > time.time() - 300]
            LOGIN_ATTEMPTS[remote] = recent
            if len(recent) >= 8:
                self.send_json(429, {"error": "Demasiados intentos. Espera cinco minutos."}); return
            try:
                data = self.read_json()
            except (ValueError, json.JSONDecodeError) as exc:
                self.send_json(400, {"error": str(exc)}); return
            if not hmac.compare_digest(str(data.get("password", "")), ADMIN_PASSWORD):
                recent.append(time.time()); LOGIN_ATTEMPTS[remote] = recent
                self.send_json(401, {"error": "Contraseña incorrecta."}); return
            sid = secrets.token_urlsafe(32)
            SESSIONS[sid] = time.time() + 8 * 60 * 60
            signature = hmac.new(SESSION_KEY, sid.encode(), hashlib.sha256).hexdigest()
            secure_flag = "; Secure" if COOKIE_SECURE else ""
            self.send_json(200, {"ok": True}, {"Set-Cookie": f"cafe_admin={sid}.{signature}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800{secure_flag}"})
            return
        if path == "/api/logout":
            sid = self.session_id()
            if sid: SESSIONS.pop(sid, None)
            secure_flag = "; Secure" if COOKIE_SECURE else ""
            self.send_json(200, {"ok": True}, {"Set-Cookie": f"cafe_admin=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0{secure_flag}"})
            return
        if path == "/api/events/register":
            try:
                data = self.read_json()
                event_id = int(data.get("eventId", 0))
                name = clean_text(data.get("name"), 100)
                phone = re.sub(r"[\s()+-]", "", clean_text(data.get("phone"), 30))
                email = clean_text(data.get("email"), 160)
                if not name or not re.fullmatch(r"\d{8,15}", phone):
                    raise ValueError("Escribe tu nombre y un teléfono válido (8 a 15 dígitos).")
                if email and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
                    raise ValueError("El correo no parece válido.")
            except (ValueError, json.JSONDecodeError) as exc:
                self.send_json(400, {"error": str(exc)}); return
            with connect_db() as db:
                db.begin()
                row = db.execute("SELECT * FROM events WHERE id=%s FOR UPDATE", (event_id,)).fetchone()
                if not row:
                    self.send_json(404, {"error": "Evento no encontrado."}); return
                now = datetime.now().replace(second=0, microsecond=0)
                if row["status"] != "active" or row["starts_at"] <= now:
                    db.execute("UPDATE events SET status='finished' WHERE id=%s AND starts_at<=%s", (event_id, now))
                    self.send_json(409, {"error": "El registro de este evento está cerrado."}); return
                count = db.execute("SELECT COUNT(*) AS total FROM registrations WHERE event_id=%s", (event_id,)).fetchone()["total"]
                if count >= row["capacity"]:
                    self.send_json(409, {"error": "El evento ya alcanzó su cupo."}); return
                try:
                    db.execute("INSERT INTO registrations(event_id,name,phone,email) VALUES(%s,%s,%s,%s)", (event_id, name, phone, email))
                except IntegrityError:
                    self.send_json(409, {"error": "Ese teléfono ya está registrado para este evento."}); return
                count += 1
                self.send_json(201, {"ok": True, "message": "Tu registro quedó confirmado.", "available": max(0, row["capacity"] - count)})
            return
        if path == "/api/admin/events":
            if not self.require_admin() or not self.check_origin(): return
            self.save_event(None); return
        self.send_json(404, {"error": "Ruta no encontrada."})

    def save_event(self, event_id: int | None) -> None:
        try:
            data = self.read_json()
            name = clean_text(data.get("name"), 120)
            description = str(data.get("description", "")).strip()[:5000]
            starts_at = str(data.get("startsAt", "")).strip()
            capacity = int(data.get("capacity", 0))
            status = data.get("status", "active")
            if not name or not description:
                raise ValueError("El nombre y la descripción son obligatorios.")
            starts_at = datetime.strptime(starts_at, "%Y-%m-%dT%H:%M")
            if capacity < 1 or capacity > 10000:
                raise ValueError("El cupo debe estar entre 1 y 10,000 personas.")
            if status not in ("active", "finished"):
                raise ValueError("Estado no válido.")
            image = image_from_data_url(data.get("imageData")) if data.get("imageData") else data.get("image")
            if image and (not isinstance(image, str) or not re.fullmatch(r"/uploads/[a-f0-9]+\.(?:jpg|png|webp)", image)):
                raise ValueError("Imagen no válida.")
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": str(exc)}); return
        with connect_db() as db:
            if event_id is not None and not db.execute("SELECT id FROM events WHERE id=%s", (event_id,)).fetchone():
                self.send_json(404, {"error": "Evento no encontrado."}); return
            if event_id is None:
                cursor = db.execute("INSERT INTO events(name,description,starts_at,capacity,image,status) VALUES(%s,%s,%s,%s,%s,%s)", (name, description, starts_at, capacity, image, status))
                event_id = cursor.lastrowid
            else:
                db.execute("UPDATE events SET name=%s,description=%s,starts_at=%s,capacity=%s,image=%s,status=%s WHERE id=%s", (name, description, starts_at, capacity, image, status, event_id))
            row = db.execute("SELECT * FROM events WHERE id=%s", (event_id,)).fetchone()
            self.send_json(201 if self.command == "POST" else 200, {"event": event_row(db, row)})

    def do_PUT(self) -> None:
        match = re.fullmatch(r"/api/admin/events/(\d+)", urlparse(self.path).path)
        if not match:
            self.send_json(404, {"error": "Ruta no encontrada."}); return
        if not self.require_admin() or not self.check_origin(): return
        self.save_event(int(match.group(1)))

    def do_DELETE(self) -> None:
        match = re.fullmatch(r"/api/admin/events/(\d+)", urlparse(self.path).path)
        if not match:
            self.send_json(404, {"error": "Ruta no encontrada."}); return
        if not self.require_admin() or not self.check_origin(): return
        with connect_db() as db:
            db.execute("DELETE FROM events WHERE id=%s", (int(match.group(1)),))
        self.send_json(200, {"ok": True})

    def do_OPTIONS(self) -> None:
        self.respond(204, b"", headers={"Allow": "GET, POST, PUT, DELETE, OPTIONS"})


if __name__ == "__main__":
    initialize_db()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    print(f"API de eventos en http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
