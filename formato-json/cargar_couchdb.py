#!/usr/bin/env python3
"""
Carga mundial_2026.json en CouchDB y crea el design document con las vistas.

Base de datos : jugadores
Design doc    : losjugadores
Vistas        : por_club, por_goles, por_partidos

Credenciales leidas desde ../.env:
    COUCHDB_USER     (default: admin)
    COUCHDB_PASSWORD (default: admin)
    COUCHDB_PORT     (default: 5985)

Uso:
    python cargar_couchdb.py
"""

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Carga .env desde la raiz del proyecto (un nivel sobre formato-json/)
load_dotenv(Path(__file__).parent.parent / ".env")

_user     = os.getenv("COUCHDB_USER", "admin")
_password = os.getenv("COUCHDB_PASSWORD", "admin")
_port     = os.getenv("COUCHDB_PORT", "5985")
BASE_URL  = f"http://localhost:{_port}"
AUTH      = (_user, _password)

JSON_FILE     = Path(__file__).parent / "mundial_2026.json"
DB_NAME       = "jugadores"
DESIGN_DOC_ID = "_design/losjugadores"

VIEWS = {
    "por_club": "function(doc) {\n  if (doc.club_actual) {\n    emit(doc.club_actual, doc);\n  }\n}",
    "por_goles": "function(doc) {\n  if (doc.goles) {\n    emit(doc.goles, doc);\n  }\n}",
    "por_partidos": "function(doc) {\n  if (doc.partidos) {\n    emit(doc.partidos, doc);\n  }\n}",
}


def crear_base_datos():
    url = f"{BASE_URL}/{DB_NAME}"
    resp = requests.get(url, auth=AUTH)
    if resp.status_code == 404:
        requests.put(url, auth=AUTH).raise_for_status()
        # Do NOT set _security on this database — access is controlled at server level only.
        print(f"[OK] Base de datos '{DB_NAME}' creada.")
    elif resp.status_code == 200:
        print(f"[OK] Base de datos '{DB_NAME}' ya existe.")
    else:
        resp.raise_for_status()


def limpiar_permisos():
    url = f"{BASE_URL}/{DB_NAME}/_security"
    empty_security = {"admins": {"names": [], "roles": []},
                      "members": {"names": [], "roles": []}}
    requests.put(url, json=empty_security, auth=AUTH).raise_for_status()
    print(f"[OK] Permisos de '{DB_NAME}' limpiados (sin restricciones por rol).")


def cargar_documentos():
    if not JSON_FILE.exists():
        print(f"[ERROR] No se encontro {JSON_FILE}. Ejecuta primero generar_json.py.")
        sys.exit(1)

    data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    resp = requests.post(f"{BASE_URL}/{DB_NAME}/_bulk_docs", json=data, auth=AUTH)
    resp.raise_for_status()

    results = resp.json()
    ok_count  = sum(1 for r in results if r.get("ok"))
    err_count = len(results) - ok_count
    print(f"[OK] Documentos insertados: {ok_count}/{len(results)}")
    if err_count:
        print(f"[WARN] Documentos con error: {err_count} (pueden ser duplicados si ya existen)")


def crear_vistas():
    design_doc = {
        "_id": DESIGN_DOC_ID,
        "language": "javascript",
        "views": {name: {"map": fn} for name, fn in VIEWS.items()},
    }

    url = f"{BASE_URL}/{DB_NAME}/{DESIGN_DOC_ID}"
    resp = requests.get(url, auth=AUTH)
    if resp.status_code == 200:
        design_doc["_rev"] = resp.json()["_rev"]
        print("[INFO] Design document existente, actualizando...")

    requests.put(url, json=design_doc, auth=AUTH).raise_for_status()
    print(f"[OK] Design document '{DESIGN_DOC_ID}' creado con vistas: {', '.join(VIEWS)}")


def main():
    print(f"Conectando a CouchDB en {BASE_URL} (usuario: {_user}) ...")
    crear_base_datos()
    limpiar_permisos()
    cargar_documentos()
    crear_vistas()
    print("\nProceso completado exitosamente!")
    print(f"  Vistas disponibles en: {BASE_URL}/{DB_NAME}/{DESIGN_DOC_ID}/_view/<vista>")


if __name__ == "__main__":
    main()
