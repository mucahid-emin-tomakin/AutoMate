#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PDFMint.py

# ============================== STDLIB-IMPORTS ==============================

import atexit
import base64
import gc
import os
import re
import shutil
import subprocess
import sys
import time

from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ============================== STDLIB-IMPORTS ==============================
# ============================== CONFIGURATION ==============================

BASE_DIR                = Path(__file__).resolve().parent.parent
CACHE_DIR               = BASE_DIR / ".cache"
BOOTSTRAP_FLAG          = BASE_DIR / ".cache" / ".bootstrap_done"
VENV_DIR                = BASE_DIR / ".venv"
VENV_PYTHON             = VENV_DIR / "Scripts" / "python.exe"
MIN_PYTHON              = (3, 12)

INPUT_DIR               = BASE_DIR / "input"
OUTPUT_DIR              = BASE_DIR / "output"
MODEL_DIR               = BASE_DIR / "models"

SERVER_HOST             = "127.0.0.1"
SERVER_PORT             = 8080
SERVER_URL              = f"http://{SERVER_HOST}:{SERVER_PORT}/v1"

VISION_PORT             = 8081
VISION_URL              = f"http://{SERVER_HOST}:{VISION_PORT}/v1"
VISION_MODEL            = "ggml-org/Qwen2.5-VL-3B-Instruct-GGUF"

GGUF_MODEL              = "GLM-OCR-Q8_0.gguf"
GGUF_MMPROJ             = "mmproj-GLM-OCR-Q8_0.gguf"
HF_REPO                 = "ggml-org/GLM-OCR-GGUF"

MIN_TEXT_CHARS_PER_PAGE = 50
DETECTION_SAMPLE_PAGES  = 3

OCR_DPI                 = 96
OCR_PROMPT              = "OCR"
OCR_MAX_TOKENS          = 2048
OCR_PAUSE_SECONDS       = 0.5

MARKER_MODE             = "fast"
MARKER_CONFIG           = {"mode":                      MARKER_MODE,
                           "keep_pagefooter_in_output": True,
                           "paginate_output":           True,}

REQUIRED_PACKAGES       = {"pymupdf":                   "fitz",
                           "pymupdf4llm":               "pymupdf4llm",
                           "openai":                    "openai",
                           "huggingface_hub":           "huggingface_hub",
                           "marker-pdf":                "marker",}

PAGE_MARKER_RE          = re.compile(r"<!--\s*Seite\s+(\d+)(?:\s*:\s*FEHLER[^>]*)?\s*-->",
                          re.IGNORECASE,)
PAGE_ERROR_RE           = re.compile(r"<!--\s*Seite\s+(\d+)\s*:\s*FEHLER[^>]*-->",
                          re.IGNORECASE,)

# ============================== CONFIGURATION ==============================
# ============================== ENVIRONMENT ==============================

os.environ.update({
    "HF_HOME":                         str(CACHE_DIR / "huggingface"),
    "HF_HUB_CACHE":                    str(CACHE_DIR / "huggingface" / "hub"),
    "HF_HUB_DISABLE_SYMLINKS_WARNING": "1",
    "PIP_CACHE_DIR":                   str(CACHE_DIR / "pip"),
    "TORCH_HOME":                      str(CACHE_DIR / "torch"),
    "DATALAB_CACHE_DIR":               str(CACHE_DIR / "datalab"),
    "MODEL_CACHE_DIR":                 str(CACHE_DIR / "datalab" / "models"),
    "XDG_CACHE_HOME":                  str(CACHE_DIR),
    "LLAMA_CACHE":                     str(CACHE_DIR / "llama.cpp"),
    "SURYA_INFERENCE_BACKEND":         "llamacpp",
    "SURYA_INFERENCE_KEEP_ALIVE":      "1",
    "PYTHONIOENCODING":                "utf-8",
    "PYTHONUTF8":                      "1",
})

# ============================== ENVIRONMENT ==============================
# ============================== GLOBAL STATE ==============================

_marker_converter  = None
_llama_process     = None
_llama_log_file    = None
_llama_we_started  = False
_vision_process    = None
_vision_log_file   = None
_vision_we_started = False

STATS = {
    "text_pdfs":        0,
    "scan_pdfs":        0,
    "images_total":     0,
    "images_ok":        0,
    "printed_pages":    0,
    "pages_ok":         0,
    "pages_failed":     0,
    "pages_skipped":    0,
}

# ============================== GLOBAL STATE ==============================
# ============================== TERMINAL HELPERS ==============================

LINE_DOUBLE = "═" * 64
LINE_SINGLE = "─" * 64

# Gibt einen Banner mit doppelter Trennlinie aus
def banner(title: str) -> None:
    print()
    print(LINE_DOUBLE)
    print(f"  {title}")
    print(LINE_DOUBLE)
    print()

# Gibt einen Phasen-Header mit einfacher Trennlinie aus
def phase(num: int, title: str) -> None:
    print()
    print(LINE_SINGLE)
    print(f"  PHASE {num}: {title}")
    print(LINE_SINGLE)
    print()

# Gibt eine Erfolgsmeldung aus
def ok(msg: str, indent: int = 1) -> None:
    print(f"{'  ' * indent}✓ {msg}")

# Gibt eine Info-Meldung aus
def info(msg: str, indent: int = 1) -> None:
    print(f"{'  ' * indent}ℹ {msg}")

# Gibt eine Warnung aus
def warn(msg: str, indent: int = 1) -> None:
    print(f"{'  ' * indent}⚠ {msg}")

# Gibt eine Fehlermeldung aus
def err(msg: str, indent: int = 1) -> None:
    print(f"{'  ' * indent}✗ {msg}")

# Gibt einen Schritt mit Pfeil aus
def step(msg: str, indent: int = 0) -> None:
    print(f"{'  ' * indent}▶ {msg}")

# Gibt einen Aufzählungspunkt aus
def bullet(msg: str, indent: int = 2) -> None:
    print(f"{'  ' * indent}• {msg}")

# Gibt eine formatierte Tabelle mit ausgerichteten Spalten aus
def summary_table(rows: list[tuple[str, str]]) -> None:
    if not rows:
        return
    width = max(len(label) for label, _ in rows) + 2
    print()
    for label, value in rows:
        print(f"  {label.ljust(width)}  {value}")
    print()

# ============================== TERMINAL HELPERS ==============================
# ============================== BOOTSTRAP ==============================

# Prüft, ob das Skript aktuell in der Projekt-venv läuft
def _is_in_venv() -> bool:
    try:
        return Path(sys.executable).resolve() == VENV_PYTHON.resolve()
    except Exception:
        return False

# Ermittelt fehlende Python-Pakete in der venv
def _find_missing_packages() -> list[str]:
    code = (
        "import importlib.util\n"
        "packages = " + repr(REQUIRED_PACKAGES) + "\n"
        "missing = [name for name, module in packages.items() "
        "if importlib.util.find_spec(module) is None]\n"
        "print('\\n'.join(missing))"
    )
    result = subprocess.run(
        [str(VENV_PYTHON), "-c", code],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        return list(REQUIRED_PACKAGES.keys())
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]

# Richtet venv und Python-Pakete ein (läuft nur beim ersten Start)
def bootstrap() -> None:
    if BOOTSTRAP_FLAG.exists():
        return
    
    banner("🍃 PDFMint")

    print("▸ Projekt-Verzeichnisse")
    for d in (CACHE_DIR, CACHE_DIR / "llama.cpp", MODEL_DIR, INPUT_DIR, OUTPUT_DIR):
        d.mkdir(parents=True, exist_ok=True)
    ok("Verzeichnisse bereit")

    print()
    print("▸ Virtuelle Umgebung")

    if VENV_PYTHON.exists():
        ok(f"venv vorhanden")
    else:
        if sys.version_info < MIN_PYTHON:
            err(f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ benötigt. "
                f"Aktuell: {sys.version_info.major}.{sys.version_info.minor}")
            sys.exit(1)

        info("Erstelle venv...")
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=False,
        )
        if result.returncode != 0 or not VENV_PYTHON.exists():
            err("venv konnte nicht erstellt werden.")
            sys.exit(1)
        ok("venv erstellt")

    if not _is_in_venv():
        info("Starte Skript in venv neu...")
        result = subprocess.run(
            [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]],
            check=False,
        )
        sys.exit(result.returncode)

    print()
    print("▸ Python-Pakete")
    missing = _find_missing_packages()

    if missing:
        warn(f"Fehlende Pakete: {', '.join(missing)}")
        info("Installiere Pakete (kann 10–15 Minuten dauern)...")
        subprocess.run(
            [str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
            check=False,
        )
        result = subprocess.run(
            [str(VENV_PYTHON), "-m", "pip", "install",
             "--disable-pip-version-check", *missing],
            check=False,
        )
        if result.returncode != 0:
            err("Paketinstallation fehlgeschlagen.")
            sys.exit(1)
        ok("Pakete installiert")
        info("Starte Skript neu...")
        result = subprocess.run(
            [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]],
            check=False,
        )
        sys.exit(result.returncode)

    ok("Alle Pakete vorhanden")
    print()

    BOOTSTRAP_FLAG.parent.mkdir(parents=True, exist_ok=True)
    BOOTSTRAP_FLAG.touch()
    
bootstrap()

# ============================== BOOTSTRAP ==============================
# ============================== EXTERNAL IMPORTS ==============================

import pymupdf as fitz
from openai import OpenAI

# ============================== EXTERNAL IMPORTS ==============================
# ============================== API CLIENTS ==============================

client = OpenAI(
    base_url=SERVER_URL,
    api_key="sk-no-key-required",
    timeout=180,
    max_retries=1,
)
vision_client = OpenAI(
    base_url=VISION_URL,
    api_key="sk-no-key-required",
    timeout=180,
    max_retries=1,
)

# ============================== API CLIENTS ==============================
# ============================== DIRECTORY HELPERS ==============================

# Legt alle benötigten Projektverzeichnisse an
def ensure_directories() -> None:
    for d in (INPUT_DIR, OUTPUT_DIR, MODEL_DIR, CACHE_DIR):
        d.mkdir(parents=True, exist_ok=True)

# ============================== DIRECTORY HELPERS ==============================
# ============================== CACHE MIGRATION ==============================

# Findet einen freien Dateinamen mit Suffix .preserved-N
def _unique_destination(path: Path) -> Path:
    if not path.exists():
        return path
    index = 1
    while True:
        candidate = path.with_name(f"{path.name}.preserved-{index}")
        if not candidate.exists():
            return candidate
        index += 1

# Verschiebt Cache-Inhalte ohne vorhandene Dateien zu überschreiben
def move_without_overwrite(source: Path, destination: Path) -> None:
    if source.is_dir() and not source.is_symlink():
        if not destination.exists():
            shutil.move(str(source), str(destination))
            return
        if destination.is_dir():
            for item in list(source.iterdir()):
                move_without_overwrite(item, destination / item.name)
            try:
                source.rmdir()
            except OSError:
                pass
            return
    destination = _unique_destination(destination)
    shutil.move(str(source), str(destination))

# ============================== CACHE MIGRATION ==============================
# ============================== DATALAB JUNCTION ==============================

# Prüft, ob ein Pfad ein Windows-Reparse-Point (Junction) ist
def _is_reparse_point(path: Path) -> bool:
    if os.name != "nt":
        return False
    import ctypes
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
    return attrs != -1 and bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)

# Entfernt eine Junction, ohne das Zielverzeichnis zu löschen
def _remove_junction_only(path: Path) -> None:
    if not _is_reparse_point(path):
        return
    result = subprocess.run(
        ["cmd", "/c", "rmdir", str(path)],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"Junction konnte nicht entfernt werden: {result.stderr}")

# Erstellt eine temporäre Junction für den Datalab-Cache
def setup_datalab_junction() -> None:
    if os.name != "nt":
        info("Datalab-Junction wird nur unter Windows verwendet")
        return

    user_datalab    = Path.home() / ".cache" / "datalab"
    project_datalab = CACHE_DIR / "datalab"

    project_datalab.mkdir(parents=True, exist_ok=True)
    user_datalab.parent.mkdir(parents=True, exist_ok=True)

    if os.path.lexists(user_datalab):
        if _is_reparse_point(user_datalab):
            try:
                if user_datalab.resolve(strict=True) == project_datalab.resolve():
                    ok(f"Junction bereits vorhanden")
                    return
            except OSError:
                pass
            info("Entferne alte Junction...")
            _remove_junction_only(user_datalab)
        else:
            if not user_datalab.is_dir():
                raise RuntimeError(f"{user_datalab} ist kein Ordner.")
            info(f"Sichere vorhandenen Cache...")
            for item in list(user_datalab.iterdir()):
                move_without_overwrite(item, project_datalab / item.name)
            try:
                user_datalab.rmdir()
            except OSError as e:
                raise RuntimeError(f"Cache-Ordner gesperrt: {e}")

    result = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(user_datalab), str(project_datalab)],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"Junction fehlgeschlagen: {result.stderr}")
    if not _is_reparse_point(user_datalab):
        raise RuntimeError("Junction nicht verifiziert.")
    if user_datalab.resolve() != project_datalab.resolve():
        raise RuntimeError("Junction zeigt auf unerwartetes Ziel.")
    ok(f"Junction verifiziert")

# Entfernt die temporäre Datalab-Junction
def remove_datalab_junction() -> None:
    if os.name != "nt":
        return
    user_datalab = Path.home() / ".cache" / "datalab"
    if not _is_reparse_point(user_datalab):
        return
    try:
        _remove_junction_only(user_datalab)
        ok(f"Junction entfernt")
    except Exception as e:
        warn(f"Junction-Entfernung fehlgeschlagen: {e}")


# ============================== DATALAB JUNCTION ==============================
# ============================== MODEL DOWNLOADS ==============================

# Lädt fehlende GLM-OCR-Modelle bei Bedarf herunter
def ensure_gguf_models() -> None:
    from huggingface_hub import hf_hub_download

    files = (GGUF_MODEL, GGUF_MMPROJ)
    missing = [f for f in files if not (MODEL_DIR / f).is_file()]

    if not missing:
        ok("GLM-OCR-Modelle vorhanden")
        return

    info(f"GLM-OCR-Modelle fehlen ({len(missing)}/2), lade herunter...")
    for filename in missing:
        bullet(f"{filename}")
        try:
            hf_hub_download(repo_id=HF_REPO, filename=filename, local_dir=str(MODEL_DIR))
        except Exception as e:
            raise RuntimeError(f"GGUF-Download fehlgeschlagen: {filename}\n{e}")
    ok("GLM-OCR-Modelle bereit")

# Prüft und erstellt die Grundumgebung (Verzeichnisse + Modelle)
def ensure_environment() -> None:
    ensure_directories()
    ensure_gguf_models()

# ============================== MODEL DOWNLOADS ==============================
# ============================== SERVER HELPERS ==============================

# Prüft, ob llama-server im PATH verfügbar ist und gibt den Pfad zurück
def _check_llama_server() -> str:
    executable = shutil.which("llama-server")
    if not executable:
        raise RuntimeError(
            "llama-server wurde nicht gefunden.\n"
            "  Bitte installieren mit:\n"
            "    winget install ggml.llamacpp"
        )
    return executable

# Prüft, ob ein API-Server antwortet und Modelle meldet
def _api_alive(api_client: OpenAI) -> bool:
    try:
        return bool(api_client.models.list().data)
    except Exception:
        return False

# Prüft, ob der Server das erwartete Modell meldet
def _verify_model(api_client: OpenAI, expected: str) -> None:
    try:
        models = api_client.models.list()
        if not models.data:
            raise RuntimeError("Server meldet keine geladenen Modelle.")
        ids = [str(m.id) for m in models.data]
        if not any(expected.lower() in mid.lower() for mid in ids):
            warn(f"Modell-ID '{expected}' nicht direkt gefunden: {ids}")
    except Exception as e:
        raise RuntimeError(f"Modellprüfung fehlgeschlagen: {e}")

# ============================== SERVER HELPERS ==============================
# ============================== LLAMA SERVER LIFECYCLE ==============================

# Prüft, ob der GLM-OCR-Server aktuell läuft
def llama_server_alive() -> bool:
    return _api_alive(client)

# Startet den GLM-OCR-Server über llama-server
def start_llama_server() -> None:
    global _llama_process, _llama_log_file, _llama_we_started

    if llama_server_alive():
        info("GLM-OCR-Server läuft bereits")
        _llama_we_started = False
        _verify_model(client, "GLM-OCR")
        return

    executable  = _check_llama_server()
    model_path  = MODEL_DIR / GGUF_MODEL
    mmproj_path = MODEL_DIR / GGUF_MMPROJ

    if not model_path.is_file() or not mmproj_path.is_file():
        raise RuntimeError(f"GLM-OCR-Dateien fehlen in {MODEL_DIR}")

    cmd = [
        executable,
        "-m", str(model_path),
        "--mmproj", str(mmproj_path),
        "-c", "12000",
        "-ngl", "99",
        "--flash-attn", "off",
        "-fit", "off",
        "--host", SERVER_HOST,
        "--port", str(SERVER_PORT),
    ]
    log_path = MODEL_DIR / "llama-server.log"
    _llama_log_file = open(log_path, "w", encoding="utf-8")
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0

    info("Starte llama-server (GLM-OCR)...")
    _llama_process = subprocess.Popen(
        cmd, stdout=_llama_log_file, stderr=subprocess.STDOUT,
        creationflags=creationflags,
    )
    _llama_we_started = True

    try:
        for i in range(180):
            if _llama_process.poll() is not None:
                raise RuntimeError(f"llama-server beendet. Log: {log_path}")
            if llama_server_alive():
                _verify_model(client, "GLM-OCR")
                ok(f"GLM-OCR bereit (nach {i+1}s)")
                return
            time.sleep(1)
        raise RuntimeError(f"GLM-OCR nicht bereit. Log: {log_path}")
    except Exception:
        stop_llama_server()
        raise

# Stoppt den GLM-OCR-Server
def stop_llama_server() -> None:
    global _llama_process, _llama_log_file, _llama_we_started

    if _llama_we_started and _llama_process is not None:
        info("Stoppe llama-server...")
        try:
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(_llama_process.pid)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15,
                )
            else:
                _llama_process.terminate()
                _llama_process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            _llama_process.kill()
        except Exception as e:
            warn(f"Stop-Fehler: {e}")

    _llama_process    = None
    _llama_we_started = False

    if _llama_log_file is not None:
        try:
            _llama_log_file.close()
        except Exception:
            pass
        _llama_log_file = None

# ============================== LLAMA SERVER LIFECYCLE ==============================
# ============================== VISION SERVER LIFECYCLE ==============================

# Prüft, ob der Vision-Server aktuell läuft
def vision_server_alive() -> bool:
    return _api_alive(vision_client)

# Startet den Qwen2.5-VL-Vision-Server über llama-server
def start_vision_server() -> None:
    global _vision_process, _vision_log_file, _vision_we_started

    if vision_server_alive():
        info("Vision-Server läuft bereits")
        _vision_we_started = False
        _verify_model(vision_client, "Qwen2.5-VL")
        return

    executable = _check_llama_server()
    cmd = [
        executable,
        "-hf", VISION_MODEL,
        "-c", "4096",
        "--host", SERVER_HOST,
        "--port", str(VISION_PORT),
    ]
    log_path = MODEL_DIR / "vision-server.log"
    _vision_log_file = open(log_path, "w", encoding="utf-8")
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0

    info("Starte Vision-Server (Qwen2.5-VL)...")
    info("Erststart: Modell-Download kann einige Minuten dauern.", indent=2)

    _vision_process = subprocess.Popen(
        cmd, stdout=_vision_log_file, stderr=subprocess.STDOUT,
        creationflags=creationflags,
    )
    _vision_we_started = True

    try:
        for i in range(1800):
            if _vision_process.poll() is not None:
                raise RuntimeError(f"Vision-Server beendet. Log: {log_path}")
            if vision_server_alive():
                _verify_model(vision_client, "Qwen2.5-VL")
                ok(f"Vision-Server bereit (nach {i+1}s)")
                return
            if (i + 1) % 30 == 0:
                bullet(f"warte noch ({i+1}s)")
            time.sleep(1)
        raise RuntimeError(f"Vision-Server nicht bereit. Log: {log_path}")
    except Exception:
        stop_vision_server()
        raise

# Stoppt den Vision-Server
def stop_vision_server() -> None:
    global _vision_process, _vision_log_file, _vision_we_started

    if _vision_we_started and _vision_process is not None:
        info("Stoppe Vision-Server...")
        try:
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(_vision_process.pid)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15,
                )
            else:
                _vision_process.terminate()
                _vision_process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            _vision_process.kill()
        except Exception as e:
            warn(f"Stop-Fehler: {e}")

    _vision_process    = None
    _vision_we_started = False

    if _vision_log_file is not None:
        try:
            _vision_log_file.close()
        except Exception:
            pass
        _vision_log_file = None

# ============================== VISION SERVER LIFECYCLE ==============================
# ============================== MARKER MANAGEMENT ==============================

# Lädt den Marker-Converter (einmalig)
def _get_marker_converter():
    global _marker_converter
    if _marker_converter is None:
        info("Lade Marker-Modelle...")
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        _marker_converter = PdfConverter(
            artifact_dict=create_model_dict(),
            config=MARKER_CONFIG,
        )
        ok("Marker-Modelle bereit")
    return _marker_converter

# Gibt die Marker-Modelle aus dem GPU-Speicher frei
def release_marker_models() -> None:
    global _marker_converter
    if _marker_converter is None:
        return
    info("Gebe Marker-Modelle frei...")
    _marker_converter = None
    gc.collect()
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass

# ============================== MARKER MANAGEMENT ==============================
# ============================== PDF RECOGNITION ==============================

# Prüft, ob eine PDF einen nutzbaren Textlayer hat
def pdf_has_text_layer(pdf_path: Path) -> bool:
    with fitz.open(pdf_path) as doc:
        sample = min(DETECTION_SAMPLE_PAGES, doc.page_count)
        if sample == 0:
            return False
        total = sum(len(doc[i].get_text().strip()) for i in range(sample))
        return (total / sample) >= MIN_TEXT_CHARS_PER_PAGE

# ============================== PDF RECOGNITION ==============================
# ============================== MARKER CONVERSION ==============================

# Konvertiert eine PDF mit Marker zu Markdown und speichert Bilder
def convert_with_marker(pdf_path: Path, img_dir: Path) -> tuple[str, dict]:
    from marker.output import text_from_rendered
    converter = _get_marker_converter()
    
    saved_argv = sys.argv.copy()
    try:
        sys.argv = [""]
        rendered = converter(str(pdf_path))
    finally:
        sys.argv = saved_argv
    
    text, _, images = text_from_rendered(rendered)

    image_map = {}
    if images:
        img_dir.mkdir(parents=True, exist_ok=True)
        for name, obj in images.items():
            try:
                path = img_dir / name
                path.parent.mkdir(parents=True, exist_ok=True)
                obj.save(path)
                image_map[name] = path
            except Exception as e:
                warn(f"Bild {name}: {e}")

    ok(f"Marker fertig ({len(text):,} Zeichen, {len(image_map)} Bild(er))")
    return text, image_map

# ============================== MARKER CONVERSION ==============================
# ============================== PRINTED PAGE NUMBERS ==============================

# Fügt gedruckte Seitenzahlen als Kommentar in die Markdown-Datei ein
def inject_printed_page_numbers(pdf_path: Path, md_path: Path) -> int:
    printed_numbers = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            rect = page.rect
            footer_rect = fitz.Rect(rect.x0, rect.y1 * 0.85, rect.x1, rect.y1)
            footer_text = page.get_text("text", clip=footer_rect).strip()
            match = re.search(r"\b(\d{1,4})\b", footer_text)
            printed_numbers.append(int(match.group(1)) if match else None)

    if not any(n is not None for n in printed_numbers):
        info("Keine gedruckten Seitenzahlen gefunden")
        return 0

    text = md_path.read_text(encoding="utf-8")

    marker_pattern = re.compile(
        r"<!--\s*(?:Seite|Page)\s*:?\s*(\d+)\s*-->"
        r"|\{(\d+)\}"
        r"|<!--\s*PDF-Seite\s+(\d+)[^>]*-->",
        re.IGNORECASE,
    )

    def replace_marker(match):
        marker_page = int(next(v for v in match.groups() if v is not None))
        idx = marker_page - 1
        if not 0 <= idx < len(printed_numbers):
            return match.group(0)
        printed = printed_numbers[idx]
        if printed is None:
            return match.group(0)
        return f"<!-- PDF-Seite {marker_page} | Druckseite {printed} -->"

    new_text, count = marker_pattern.subn(replace_marker, text)
    if count:
        md_path.write_text(new_text, encoding="utf-8")
        ok(f"Seitenmarkierungen verarbeitet ({count})")
    else:
        info("Keine unterstützten Marker-Seitenangaben gefunden")
    return count

# ============================== PRINTED PAGE NUMBERS ==============================
# ============================== TEXT PDF PROCESSING ==============================

# Verarbeitet eine Text-PDF komplett (Marker + Seitenzahlen)
def process_text_pdf(pdf_path: Path, out_dir: Path) -> tuple[Path, str, dict]:
    md_path = out_dir / f"{pdf_path.stem}.md"
    img_dir = out_dir / "images"

    text, image_map = convert_with_marker(pdf_path, img_dir)

    md_path.write_text(f"# {pdf_path.stem}\n\n{text}", encoding="utf-8")
    count = inject_printed_page_numbers(pdf_path, md_path)
    STATS["printed_pages"] += count

    text = md_path.read_text(encoding="utf-8")
    return md_path, text, image_map

# ============================== TEXT PDF PROCESSING ==============================
# ============================== VISION IMAGE DESCRIPTION ==============================

# Beschreibt ein Bild per Vision-Modell (Qwen2.5-VL)
def describe_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    ext = image_path.suffix.lower().lstrip(".")
    mime = "image/png" if ext == "png" else f"image/{ext}"

    response = vision_client.chat.completions.create(
        model="Qwen2.5-VL-3B-Instruct",
        temperature=0,
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": (
                    "Beschreibe den Inhalt dieses Bildes präzise auf Deutsch. "
                    "Erkläre, was zu sehen ist und welche Daten oder Trends dargestellt werden."
                )},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ],
        }],
    )
    return (response.choices[0].message.content or "").strip()

# ============================== VISION IMAGE DESCRIPTION ==============================
# ============================== IMAGE REPLACEMENT ==============================

# Ersetzt Bildpfade im Markdown durch die Vision-Beschreibungen
def replace_images_with_descriptions(
    text: str, image_map: dict, descriptions: dict,
) -> str:
    for name in image_map:
        desc = descriptions.get(name, "") or "(Beschreibung nicht verfügbar)"
        replacement = f"> **Bildbeschreibung:** {desc}"
        escaped_name = re.escape(name)
        patterns = [
            re.compile(rf'!\[[^\]]*\]\([^)]*{escaped_name}(?:[?#][^)]*)?\)', re.IGNORECASE),
            re.compile(rf'<img\b[^>]*\bsrc\s*=\s*["\'][^"\']*{escaped_name}[^"\']*["\'][^>]*>', re.IGNORECASE),
        ]
        for pattern in patterns:
            text = pattern.sub(lambda _: replacement, text)
    return text

# ============================== IMAGE REPLACEMENT ==============================
# ============================== GLM-OCR ==============================

# Rendert eine PDF-Seite als Base64-Data-URL
def page_to_data_url(page: fitz.Page) -> str:
    pix = page.get_pixmap(dpi=OCR_DPI)
    b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")
    return f"data:image/png;base64,{b64}"

# OCR einer PDF-Seite per GLM-OCR
def ocr_page(page: fitz.Page) -> str:
    response = client.chat.completions.create(
        model="GLM-OCR",
        temperature=0,
        max_tokens=OCR_MAX_TOKENS,
        extra_body={"repeat_penalty": 1.05, "repeat_last_n": 256},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": OCR_PROMPT},
                {"type": "image_url", "image_url": {"url": page_to_data_url(page)}},
            ],
        }],
    )
    text = (response.choices[0].message.content or "").strip()

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) > 10:
        most_common_count = Counter(lines).most_common(1)[0][1]
        if most_common_count > 5:
            raise RuntimeError("Wiederholungsschleife erkannt")

    if len(re.findall(r"[\u4e00-\u9fff]", text)) > 20:
        raise RuntimeError("Unerwartet hoher Anteil chinesischer Zeichen")

    return text

# ============================== GLM-OCR ==============================
# ============================== OCR OUTPUT CLEANUP ==============================

# Entfernt GLM-OCR-Grounding-Tags (nur 4-stellige Koordinaten)
def strip_grounding_tags(text: str) -> str:
    text = re.sub(r"<\|det\|>.*?<\|/det\|>\s*", "", text, flags=re.DOTALL)
    text = re.sub(
        r"(?<!\w)\[\s*\d{1,5}\s*,\s*\d{1,5}\s*,\s*\d{1,5}\s*,\s*\d{1,5}\s*\](?!\w)",
        "", text,
    )
    text = re.sub(
        r"^\s*(title|text|image|chart|image_caption|image_footnote|header|footer|page_number)\s*",
        "", text, flags=re.MULTILINE | re.IGNORECASE,
    )
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

# ============================== OCR OUTPUT CLEANUP ==============================
# ============================== OCR RESUME MANAGEMENT ==============================

# Liefert pro Seite den letzten Verarbeitungsstatus (success/error)
def get_page_statuses(md_path: Path) -> dict[int, str]:
    if not md_path.exists():
        return {}
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    statuses = {}
    for match in PAGE_MARKER_RE.finditer(text):
        page_number = int(match.group(1))
        is_error = bool(PAGE_ERROR_RE.fullmatch(match.group(0)))
        statuses[page_number] = "error" if is_error else "success"
    return statuses

# Aktualisiert den Seitenblock einer Seite (auch bei Retry)
def update_page_output(md_path: Path, page_number: int, content: str, error: bool = False) -> None:
    text = md_path.read_text(encoding="utf-8")
    marker_pattern = re.compile(
        r"<!--\s*Seite\s+(\d+)(?:\s*:\s*FEHLER[^>]*)?\s*-->",
        re.IGNORECASE,
    )
    matches = list(marker_pattern.finditer(text))
    marker_text = (
        f"<!-- Seite {page_number}: FEHLER -->"
        if error
        else f"<!-- Seite {page_number} -->"
    )
    replacement = f"\n\n{marker_text}\n\n{content}\n"

    page_matches = [m for m in matches if int(m.group(1)) == page_number]
    if page_matches:
        match = page_matches[-1]
        next_marker = next((c for c in matches if c.start() >= match.end()), None)
        end = next_marker.start() if next_marker else len(text)
        text = text[:match.start()] + replacement + text[end:]
    else:
        text += replacement
    md_path.write_text(text, encoding="utf-8")

# ============================== OCR RESUME MANAGEMENT ==============================
# ============================== SCANNED PDF PROCESSING ==============================

# Verarbeitet eine Scan-PDF seitenweise per GLM-OCR
def process_scan_pdf(pdf_path: Path, out_dir: Path) -> Path:
    md_path = out_dir / f"{pdf_path.stem}.md"

    with fitz.open(pdf_path) as doc:
        total = doc.page_count
        if total == 0:
            raise RuntimeError("PDF enthält keine Seiten.")

        if not md_path.exists():
            md_path.write_text(f"# {pdf_path.stem}\n", encoding="utf-8")

        statuses = get_page_statuses(md_path)
        already_done = sum(1 for s in statuses.values() if s == "success")

        if already_done:
            info(f"Resume: {already_done}/{total} Seiten bereits erledigt")

        for i in range(total):
            page_num = i + 1

            if statuses.get(page_num) == "success":
                STATS["pages_skipped"] += 1
                continue

            print(f"    [{page_num}/{total}] ", end="", flush=True)

            try:
                md = ocr_page(doc[i])
                md = strip_grounding_tags(md)

                if not md:
                    raise RuntimeError("OCR lieferte keinen Text")

                update_page_output(md_path, page_num, md)
                STATS["pages_ok"] += 1
                print(f"✓ {len(md)} Z.")

            except Exception as e:
                error_message = str(e).replace("-->", "").replace("\n", " ")
                update_page_output(md_path, page_num, error_message, error=True)
                STATS["pages_failed"] += 1
                print(f"✗ {error_message}")

            time.sleep(OCR_PAUSE_SECONDS)

    return md_path

# ============================== SCANNED PDF PROCESSING ==============================
# ============================== POST-PROCESSING ==============================

# Zählt fehlerhafte Seiten in einer Markdown-Datei
def count_failed_pages(md_path: Path) -> int:
    return sum(1 for s in get_page_statuses(md_path).values() if s == "error")

# Gibt den Abschlussbericht für eine PDF aus
def report_pdf(pdf: Path, md_path: Path) -> None:
    failed = count_failed_pages(md_path)
    if failed:
        warn(f"{failed} fehlerhafte Seite(n) — {md_path.name}")
    else:
        ok(f"{md_path.name}")

# Gibt eine Fehlermeldung für eine PDF aus
def report_error(pdf: Path, reason: str) -> None:
    err(f"{pdf.name}: {reason}")

# ============================== POST-PROCESSING ==============================
# ============================== VISION PHASE ==============================

# Führt die Vision-Phase aus (Bilder beschreiben per Qwen2.5-VL)
def process_vision_results(marker_results: list) -> None:
    needs_vision = any(bool(r[4]) for r in marker_results)
    if not needs_vision:
        info("Keine Bilder — Vision-Server wird nicht gestartet.")
        return

    phase(3, "Bilder beschreiben (Qwen2.5-VL)")

    try:
        start_vision_server()
    except Exception as e:
        err(f"Vision-Server konnte nicht starten: {e}")
        info("Marker-Ergebnisse bleiben ohne Bildbeschreibungen.")
        for pdf, out_dir, md_path, text, image_map in marker_results:
            if image_map:
                shutil.rmtree(out_dir / "images", ignore_errors=True)
            report_pdf(pdf, md_path)
        return

    try:
        for pdf, out_dir, md_path, text, image_map in marker_results:
            if not image_map:
                report_pdf(pdf, md_path)
                continue

            step(f"{pdf.name} ({len(image_map)} Bild(er))")
            STATS["images_total"] += len(image_map)

            try:
                descriptions = {}
                for i, (name, path) in enumerate(image_map.items(), 1):
                    print(f"    [{i}/{len(image_map)}] ", end="", flush=True)
                    try:
                        desc = describe_image(path)
                        descriptions[name] = desc
                        STATS["images_ok"] += 1
                        print(f"✓ {name} ({len(desc)} Z.)")
                    except Exception as e:
                        print(f"✗ {name}: {e}")
                        descriptions[name] = ""

                new_text = replace_images_with_descriptions(text, image_map, descriptions)
                md_path.write_text(f"# {pdf.stem}\n\n{new_text}", encoding="utf-8")
                shutil.rmtree(out_dir / "images", ignore_errors=True)
                report_pdf(pdf, md_path)

            except Exception as e:
                report_error(pdf, f"Bildbeschreibung fehlgeschlagen: {e}")

    finally:
        stop_vision_server()

# ============================== VISION PHASE ==============================
# ============================== MAIN ==============================

# Hauptfunktion: orchestriert die vier Phasen der Pipeline
def main():
    try:
        print()
        print("▸ Phase 0: Vorbereitung")

        setup_datalab_junction()
        atexit.register(remove_datalab_junction)

        ensure_directories()
        ensure_gguf_models()
        _get_marker_converter()
        release_marker_models()

        pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
        if not pdf_files:
            warn(f"Keine PDFs in {INPUT_DIR} gefunden.")
            return

        phase(1, f"PDF-Erkennung ({len(pdf_files)} Datei(en))")

        text_pdfs, scan_pdfs = [], []
        for pdf in pdf_files:
            try:
                if pdf_has_text_layer(pdf):
                    text_pdfs.append(pdf)
                    print(f"  [TEXT] {pdf.name}")
                else:
                    scan_pdfs.append(pdf)
                    print(f"  [SCAN] {pdf.name}")
            except Exception as e:
                report_error(pdf, f"PDF-Erkennung fehlgeschlagen: {e}")

        print()
        summary_table([
            ("Text-PDFs (Marker)",   str(len(text_pdfs))),
            ("Scan-PDFs (GLM-OCR)",  str(len(scan_pdfs))),
        ])

        marker_results = []
        if text_pdfs:
            phase(2, "Marker + Surya (Text-PDFs)")
            for pdf in text_pdfs:
                step(pdf.name)
                out_dir = OUTPUT_DIR / pdf.stem
                out_dir.mkdir(parents=True, exist_ok=True)
                try:
                    md_path, text, image_map = process_text_pdf(pdf, out_dir)
                    marker_results.append((pdf, out_dir, md_path, text, image_map))
                    STATS["text_pdfs"] += 1
                except Exception as e:
                    report_error(pdf, str(e))

            release_marker_models()
        else:
            info("Keine Text-PDFs.")

        process_vision_results(marker_results)

        if scan_pdfs:
            phase(4, "Scans OCR (GLM-OCR)")
            try:
                start_llama_server()
            except Exception as e:
                err(f"llama-server konnte nicht starten: {e}")
                info("OCR-Phase wird übersprungen.")
            else:
                try:
                    for pdf in scan_pdfs:
                        step(pdf.name)
                        out_dir = OUTPUT_DIR / pdf.stem
                        out_dir.mkdir(parents=True, exist_ok=True)
                        try:
                            md_path = process_scan_pdf(pdf, out_dir)
                            STATS["scan_pdfs"] += 1
                            report_pdf(pdf, md_path)
                        except Exception as e:
                            report_error(pdf, str(e))
                finally:
                    stop_llama_server()
        else:
            info("Keine Scans — GLM-OCR wird nicht gestartet.")

        banner("✓ PDFMint abgeschlossen")
        summary_table([
            ("Text-PDFs verarbeitet",  str(STATS["text_pdfs"])),
            ("Scan-PDFs verarbeitet",  str(STATS["scan_pdfs"])),
            ("Bilder beschrieben",     f"{STATS['images_ok']}/{STATS['images_total']}"),
            ("Druckseiten erkannt",    str(STATS["printed_pages"])),
            ("OCR-Seiten ok",          str(STATS["pages_ok"])),
            ("OCR-Seiten fehlerhaft",  str(STATS["pages_failed"])),
            ("OCR-Seiten übersprungen", str(STATS["pages_skipped"])),
        ])
        info(f"Ausgabe: {OUTPUT_DIR}")
        print()

    except KeyboardInterrupt:
        print()
        warn("Abbruch durch Benutzer.")
    except Exception as e:
        print()
        err(f"Kritischer Fehler: {e}")
        raise
    finally:
        stop_vision_server()
        stop_llama_server()
        release_marker_models()
        remove_datalab_junction()

# ============================== MAIN ==============================
# ============================== PROGRAM START ==============================

if __name__ == "__main__":
    main()