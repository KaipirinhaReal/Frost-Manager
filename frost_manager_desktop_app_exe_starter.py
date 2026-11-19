"""
Frost-Manager Desktop-Starter & EXE-Generator
Entwickelt von Kai Fischer
=============================================
Dieses Skript startet den Frost-Manager als eigenständiges Windows-Programm
und speichert alle Daten automatisch dauerhaft auf dem jeweiligen PC (unter
%APPDATA%/FrostManager/AppProfile).
"""

import http.server
import os
import shutil
import socket
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path

APP_TITLE = "Frost-Manager – Entwickelt von Kai Fischer"
APP_AUTHOR = "Kai Fischer"


def get_resource_path(filename: str) -> Path:
    """Findet eingebettete Dateien sowohl im normalen Lauf als auch innerhalb der fertigen .exe."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / filename
    return Path(__file__).resolve().parent / filename


def ensure_index_html_exists(script_dir: Path) -> Path:
    """Prüft, ob index.html existiert oder versehentlich als index.html.txt gespeichert wurde."""
    target = script_dir / "index.html"
    if target.exists():
        return target

    # Häufiger Windows-Fall: Datei wurde als index.html.txt oder index.htm gespeichert
    for alt_name in ["index.html.txt", "index.htm", "Frost-Manager.html", "Frost-Manager.html.txt"]:
        alt_path = script_dir / alt_name
        if alt_path.exists():
            shutil.copy2(alt_path, target)
            print(f"[INFO] '{alt_name}' wurde automatisch als 'index.html' erkannt.")
            return target

    return target


def find_free_port() -> int:
    """Sucht einen freien lokalen Port für den internen App-Server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Liefert die index.html lokal aus, ohne Konsolenfenster-Meldungen."""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        pass


def launch_app_window(url: str) -> None:
    """Öffnet die Anwendung im nativen App-Modus (ohne Browser-Adressleiste) über Edge oder Chrome."""
    candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]

    user_data_dir = Path(os.getenv("APPDATA", str(Path.home()))) / "FrostManager" / "AppProfile"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    for exe_path in candidates:
        if os.path.exists(exe_path):
            subprocess.Popen([
                exe_path,
                f"--app={url}",
                f"--user-data-dir={user_data_dir}",
                "--window-size=1340,900",
                "--disable-extensions",
            ])
            return

    webbrowser.open(url)


def build_exe_automatically() -> None:
    """Installiert bei Bedarf PyInstaller und erstellt automatisch die fertige Frost-Manager.exe."""
    script_dir = Path(__file__).resolve().parent
    html_path = ensure_index_html_exists(script_dir)

    print("=" * 60)
    print("  FROST-MANAGER EXE-GENERATOR (Entwickelt von Kai Fischer)")
    print("=" * 60)

    if not html_path.exists():
        print(f"\n[FEHLER] Die Datei 'index.html' fehlt im Ordner:\n{script_dir}")
        print("Bitte speichere die HTML-Datei als 'index.html' in denselben Ordner!")
        input("\nDrücke Enter zum Beenden...")
        return

    print("\n[1/2] Prüfe/Installiere PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])

    print("\n[2/2] Erstelle 'Frost-Manager.exe' (dauert ca. 20-40 Sekunden)...")
    sep = ";" if os.name == "nt" else ":"
    subprocess.check_call([
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--add-data=index.html{sep}.",
        "--name=Frost-Manager",
        str(Path(__file__).resolve()),
    ], cwd=str(script_dir))

    exe_file = script_dir / "dist" / "Frost-Manager.exe"
    print("\n" + "=" * 60)
    print("  FERTIG! Deine EXE wurde erfolgreich erstellt:")
    print(f"  --> {exe_file}")
    print("=" * 60)
    if os.name == "nt" and exe_file.parent.exists():
        os.startfile(str(exe_file.parent))


def main() -> None:
    if "--build" in sys.argv:
        build_exe_automatically()
        return

    html_file = get_resource_path("index.html")
    if not hasattr(sys, "_MEIPASS"):
        html_file = ensure_index_html_exists(Path(__file__).resolve().parent)

    if not html_file.exists():
        raise FileNotFoundError(f"Die Datei 'index.html' wurde nicht gefunden unter: {html_file}")

    serve_dir = str(html_file.parent)
    port = 45821
    try:
        server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", port),
            lambda *a, **kw: QuietHandler(*a, directory=serve_dir, **kw),
        )
    except OSError:
        port = find_free_port()
        server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", port),
            lambda *a, **kw: QuietHandler(*a, directory=serve_dir, **kw),
        )

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    url = f"http://127.0.0.1:{port}/index.html"
    launch_app_window(url)

    try:
        server_thread.join()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()