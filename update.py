import os
import sys
import tempfile
from pathlib import Path

import requests
from packaging.version import Version, InvalidVersion

AKTUELLE_VERSION = "1.0.0"

VERSION_URL = "https://raw.githubusercontent.com/BENUTZER/REPO/main/updates/version.txt"
UPDATE_URL = "https://raw.githubusercontent.com/BENUTZER/REPO/main/updates/app.py"


def jetzt_updaten():
    response = requests.get(UPDATE_URL, timeout=15)
    response.raise_for_status()
    neuer_code = response.content

    skript_pfad = Path(sys.argv[0]).resolve()

    # Erst vollständig in eine temporäre Datei schreiben.
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=skript_pfad.parent, delete=False
    ) as datei:
        datei.write(neuer_code)
        temp_pfad = Path(datei.name)

    # Danach die bestehende Datei ersetzen.
    os.replace(temp_pfad, skript_pfad)

    print("Update installiert. Bitte starte die App erneut.")
    # Automatischer Neustart ist hier absichtlich ausgelassen:
    # Der App-Code könnte nach update_check() sonst weiterlaufen,
    # während os.execv() den laufenden Prozess ersetzt.


def update_check():
    print(f"Aktuelle Version: {AKTUELLE_VERSION}")
    print("Prüfe auf Updates...")

    try:
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        neueste_version = Version(response.text.strip())

        if neueste_version > Version(AKTUELLE_VERSION):
            print(f"Update verfügbar: Version {neueste_version}")
            jetzt_updaten()
        else:
            print("Deine Software ist auf dem neuesten Stand.")

    except (requests.RequestException, InvalidVersion) as e:
        print(f"Update-Prüfung fehlgeschlagen: {e}")


if __name__ == "__main__":
    update_check()
    print("\n--- Willkommen in deiner App ---")
    print("App läuft im Normalbetrieb...")