#!/bin/bash
# setup.sh - Installationsskript für das Smart Plant Identification Tool

echo "=== Smart Plant Identification and Navigation Tool Setup ==="
echo "Installiere Systemabhängigkeiten..."

# System-Updates
sudo apt update

# Python tkinter für GUI
sudo apt install -y python3-tk

# Python-Abhängigkeiten installieren
echo "Installiere Python-Abhängigkeiten..."
pip install -r requirements.txt

echo "Setup abgeschlossen!"
echo ""
echo "Verwendung:"
echo "  GUI-Version:     python3 main_gui.py"
echo "  Headless-Test:   python3 test_application.py"
echo ""
echo "Hinweis: Für die GUI-Version wird ein Display benötigt."
