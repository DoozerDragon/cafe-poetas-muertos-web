"""Migra una base local eventos.sqlite3 a un esquema MySQL previamente creado."""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from pathlib import Path

import mysql.connector

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "eventos.sqlite3"


def as_datetime(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"No se encontró la base origen: {SOURCE}")
    required = ("DB_NAME", "DB_USER")
    if any(not os.environ.get(key) for key in required):
        raise SystemExit("Configura DB_NAME y DB_USER en el entorno.")

    source = sqlite3.connect(SOURCE)
    source.row_factory = sqlite3.Row
    target = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "3306")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ.get("DB_PASSWORD", ""),
        charset="utf8mb4",
    )
    try:
        cursor = target.cursor(dictionary=True)
        cursor.execute("SELECT (SELECT COUNT(*) FROM events) AS events, (SELECT COUNT(*) FROM registrations) AS registrations")
        counts = cursor.fetchone()
        if counts["events"] or counts["registrations"]:
            raise SystemExit("La base MySQL de destino no está vacía; cancelo para evitar duplicados.")

        events = source.execute("SELECT * FROM events ORDER BY id").fetchall()
        registrations = source.execute("SELECT * FROM registrations ORDER BY id").fetchall()
        event_sql = """INSERT INTO events(id,name,description,starts_at,capacity,image,status,created_at)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        registration_sql = """INSERT INTO registrations(id,event_id,name,phone,email,created_at)
                               VALUES(%s,%s,%s,%s,%s,%s)"""
        for row in events:
            cursor.execute(event_sql, (row["id"], row["name"], row["description"], as_datetime(row["starts_at"]),
                                       row["capacity"], row["image"], row["status"], as_datetime(row["created_at"])))
        for row in registrations:
            cursor.execute(registration_sql, (row["id"], row["event_id"], row["name"], row["phone"], row["email"],
                                              as_datetime(row["created_at"])))
        target.commit()
        print(f"Migración completada: {len(events)} eventos y {len(registrations)} inscripciones.")
        print("Conserva la base SQLite de origen como respaldo privado hasta verificar el sitio publicado.")
    except Exception:
        target.rollback()
        raise
    finally:
        source.close()
        target.close()


if __name__ == "__main__":
    main()
