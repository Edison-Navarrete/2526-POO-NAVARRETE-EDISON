# actividad_inventario/infraestructura/almacenamiento.py
# Requisito: Almacenamiento en archivos (guardar/cargar inventario).
# Decisión: Se usa JSON (legible) con escritura atómica (tmp + replace) para evitar corrupción.

from __future__ import annotations
from pathlib import Path
import json
from typing import Dict, Any

def cargar_json(path: Path) -> Dict[str, Any]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠ Archivo JSON inválido o corrupto. Se inicia con inventario vacío.")
        return {}
    except Exception as e:
        print(f"⚠ Error cargando JSON: {e}")
        return {}

def guardar_json(path: Path, data: Dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(path)  # Reemplazo atómico del archivo final
    except Exception as e:
        print(f"⚠ Error guardando JSON: {e}")