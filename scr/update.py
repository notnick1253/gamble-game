import json
import os
import sys
import tempfile
from pathlib import Path

import requests
from packaging.version import InvalidVersion, Version


REPO_URL = "https://raw.githubusercontent.com/notnick1253/gamble-game/main"
VERSION_URL = f"{REPO_URL}/version.txt"
MANIFEST_URL = f"{REPO_URL}/manifest.json"


def update_files():
    app_dir = Path(sys.argv[0]).resolve().parent

    # Manifest von GitHub laden.
    response = requests.get(MANIFEST_URL, timeout=15)
    response.raise_for_status()
    manifest = response.json()

    prepared_files = []

    try:
        # Alle Dateien herunterladen und zunächst temporär speichern.
        for relative_name, url in manifest["files"].items():
            relative_path = Path(relative_name)

            # Verhindert absolute Pfade und Pfade wie ../../andere_datei.
            if relative_path.is_absolute() or ".." in relative_path.parts:
                raise ValueError(f"Ungültiger Dateipfad im Manifest: {relative_name}")

            target_path = (app_dir / relative_path).resolve()

            # Das Ziel muss im Programmordner bleiben.
            if not target_path.is_relative_to(app_dir):
                raise ValueError(f"Ungültiger Dateipfad im Manifest: {relative_name}")

            download = requests.get(url, timeout=30)
            download.raise_for_status()

            target_path.parent.mkdir(parents=True, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=target_path.parent,
                delete=False,
            ) as temp_file:
                temp_file.write(download.content)
                temp_path = Path(temp_file.name)

            prepared_files.append((temp_path, target_path, relative_name))

        # Erst nachdem alle Downloads geklappt haben, Dateien ersetzen.
        # version.txt kommt zuletzt, damit die angezeigte Version zum Stand passt.
        prepared_files.sort(
            key=lambda item: item[2] == "version.txt"
        )

        for temp_path, target_path, _ in prepared_files:
            os.replace(temp_path, target_path)

        print("Update installiert. Bitte starte das Programm erneut.")

    finally:
        # Temporäre Dateien entfernen, falls beim Update etwas fehlschlägt.
        for temp_path, _, _ in prepared_files:
            temp_path.unlink(missing_ok=True)


def update_check():
    app_dir = Path(sys.argv[0]).resolve().parent
    local_version_path = app_dir / "version.txt"

    try:
        current_version_text = local_version_path.read_text(
            encoding="utf-8"
        ).strip()

        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        latest_version_text = response.text.strip()

        current_version = Version(current_version_text)
        latest_version = Version(latest_version_text)

        print(f"Aktuelle Version: {current_version}")
        print("Prüfe auf Updates...")

        if latest_version > current_version:
            print(f"Update verfügbar: Version {latest_version}")
            update_files()
        else:
            print("Deine Software ist auf dem neuesten Stand.")

    except (requests.RequestException, InvalidVersion, ValueError, KeyError) as error:
        print(f"Update-Prüfung fehlgeschlagen: {error}")

if __name__ == "__main__":
    update_check()
