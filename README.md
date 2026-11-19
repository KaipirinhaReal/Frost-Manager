# ❄️ Frost-Manager

Eine moderne, **100 % lokal laufende Gefriertruhen- und Vorratsverwaltung** für Windows und den Browser – ohne Cloud-Zwang, ohne Login und ohne Abo.

Entwickelt von **Kai Fischer (Elbtalwerk)** · Kontakt & Feedback: `elbtalwerk.kontakt@gmx.de`

---

## ✨ Funktionen

* **Mehrere Gefrierorte & Fächer:** Verwalte beliebig viele Standorte (Standard: *Küche*, *Hauswirtschaftsraum*, *Keller / Truhe*) mit übersichtlichen Standort-Tabs und Fachangabe.
* **Intelligente Kategorie- & MHD-Automatik:** Integrierte Lebensmittel-Wissensdatenbank erkennt anhand der Bezeichnung automatisch die passende Kategorie, berechnet das voraussichtliche Mindesthaltbarkeitsdatum bei −18 °C und liefert praktische Einfriertipps (alle Werte jederzeit manuell anpassbar).
* **Schnelle Bestandspflege:** Mehrfach-Anlage gleicher Portionen, Duplizieren, Bearbeiten, `+/−`-Mengensteuerung, „Verbraucht“-Button, Notizen, Suche, Sortierung und Schnellfilter für bald ablaufende Vorräte.
* **DIN-A4-Druckfunktion (Magnetwand-Liste):** Druckoptimierte Bestandslisten (gesamt oder pro Gefrierort) inklusive A4-Vollbild-Vorschau, direktem Druck, neuem Tab oder Export als eigenständige druckbare HTML-Datei.
* **Backup & Export:** Datensicherung als **JSON** (inkl. Drag-and-Drop-Import mit Wahl zwischen *Zusammenführen* und *Ersetzen*) sowie **Excel-/CSV-Export**.
* **Datenschutz & Lokale Speicherung:** Alle Daten bleiben dauerhaft auf deinem eigenen PC (`%APPDATA%/FrostManager/AppProfile` im Desktop-Modus bzw. Browser-`localStorage`). Keine Registrierung, keine Weitergabe an Dritte.

---

## 🚀 Download & Start (Windows)

### Option 1: Fertige `Frost-Manager.exe` (empfohlen, kein Python nötig)
1. Öffne rechts auf dieser Seite den Bereich **[Releases](../../releases)** und lade die aktuelle **`Frost-Manager.exe`** herunter.
2. Starte die Datei per Doppelklick – die App öffnet sich direkt im eigenen Fenster ohne Browser-Adressleiste (über Edge oder Chrome).

> **Hinweis zu Windows SmartScreen:**  
> Da die `.exe` ein kostenloses Privatprojekt ohne kommerzielles Code-Signing-Zertifikat ist, zeigt Windows beim ersten Start ggf. die Meldung *„Windows hat Ihren PC geschützt“*. Klicke dort auf **„Weitere Informationen“ → „Trotzdem ausführen“**. Alternativ kannst du den offenen Quellcode unten jederzeit selbst prüfen oder die `.exe` mit einem Befehl selbst bauen.

### Option 2: Direkt im Browser (ohne Installation)
Lade das Repository herunter und öffne einfach die **`index.html`** direkt in einem modernen Browser (Edge, Chrome, Firefox).

### Option 3: Mit Python starten oder eigene `.exe` bauen
Der Desktop-Starter benötigt zum Ausführen **ausschließlich die Python-Standardbibliothek** (Python 3.9+, keine zusätzlichen Pakete erforderlich):

```bash
# Als Desktop-App starten
python frost_manager_desktop_app_exe_starter.py

# Eigenständige Windows-EXE automatisch erstellen (installiert PyInstaller automatisch)
python frost_manager_desktop_app_exe_starter.py --build
```

Alternativ direkt über die mitgelieferte Spec-Datei:

```bash
pip install pyinstaller
pyinstaller Frost-Manager.spec
```

Die fertige ausführbare Datei landet anschließend unter `dist/Frost-Manager.exe`.

---

## 📁 Projektstruktur

| Datei | Beschreibung |
|---|---|
| `index.html` | Komplette Web-App (Oberfläche, MHD-Wissensdatenbank, DIN-A4-Druck, JSON/CSV-Backup) |
| `frost_manager_desktop_app_exe_starter.py` | Lokaler App-Server, nativer Fenster-Starter (`--app`) & integrierter `--build`-EXE-Generator |
| `Frost-Manager.spec` | Portable PyInstaller-Build-Konfiguration |
| `CHANGELOG.md` | Versionshistorie |
| `LICENSE` | MIT-Lizenz |

> **Technischer Hinweis:** Für die Darstellung von Layout und Schriftarten lädt `index.html` Tailwind CSS und Google Fonts über CDN. Deine Bestandsdaten bleiben dabei immer zu 100 % lokal auf deinem Gerät.

---

## 📄 Lizenz & Kontakt

Veröffentlicht unter der **MIT-Lizenz** (siehe [`LICENSE`](LICENSE)) – frei kopier-, teil- und weiterentwickelbar.

**Entwickler:** Kai Fischer (Elbtalwerk)  
**Feedback, Wünsche & Fehlermeldungen:** `elbtalwerk.kontakt@gmx.de`
