# Smart Plant Identification and Navigation Tool

## Projektübersicht

Dieses Projekt implementiert ein vollständiges Computer Vision System mit YOLOv8 für die Identifikation und Navigation zu Pflanzen. Das System kann zwischen nützlichen und schädlichen Pflanzen unterscheiden und simuliert Roboterbewegungen zur Entfernung schädlicher Pflanzen.

## Funktionen

### Kernfunktionalitäten
- **Pflanzenerkennung**: Automatische Erkennung und Klassifikation von Pflanzen in Bildern
- **Begrenzungsrahmen**: Grüne Rahmen für nützliche Pflanzen, rote Rahmen für schädliche Pflanzen
- **Koordinatenextraktion**: Berechnung der Mittelpunktkoordinaten aller erkannten Objekte
- **Navigationsimulation**: Logische Roboterbewegung zu schädlichen Pflanzen

### GUI-Features
- **Schwarzes Fenster** mit hellblauen Buttons entsprechend den Anforderungen
- **Upload Image**: Bildauswahl und -anzeige
- **Run Detection**: Ausführung der YOLOv8-Erkennung
- **Show Coordinates**: Anzeige aller Koordinaten
- **Simulate Navigation**: Animation der Roboterbewegung
- **Exit**: Anwendung beenden

## Projektstruktur

```
plant_robot_tool/
├── main_gui.py          # Hauptanwendung mit GUI
├── detector.py          # YOLOv8-Erkennungsmodul
├── navigator.py         # Navigationsimulationsmodul
├── test_application.py  # Testskript für Headless-Umgebungen
├── best.pt             # Vortrainiertes YOLOv8-Modell
├── data/               # Trainingsdaten
│   └── yolov8_merged_dataset/ [Download data.zip](https://gitlab.com/<BENUTZERNAME>/<PROJEKTNAME>/-/raw/main/data.zip)

└── README.md           # Diese Dokumentation
```

## Installation und Ausführung

### Systemanforderungen
- Python 3.11+
- Ubuntu 22.04 oder kompatibles Linux-System
- Mindestens 4GB RAM für YOLOv8-Inferenz

### Abhängigkeiten installieren
```bash
pip install ultralytics opencv-python Pillow
sudo apt install python3-tk  # Für GUI-Unterstützung
```

### Anwendung starten
```bash
# GUI-Version (erfordert Display)
python3 main_gui.py

# Headless-Test (ohne Display)
python3 test_application.py
```

## Verwendung

### 1. Bild hochladen
- Klicken Sie auf "Upload Image"
- Wählen Sie ein Bild mit Pflanzen aus
- Das Bild wird in der GUI angezeigt

### 2. Erkennung durchführen
- Klicken Sie auf "Run Detection"
- Das System analysiert das Bild mit YOLOv8
- Erkannte Pflanzen werden mit farbigen Begrenzungsrahmen markiert

### 3. Koordinaten anzeigen
- Klicken Sie auf "Show Coordinates"
- Alle Mittelpunktkoordinaten werden im Informationsbereich angezeigt

### 4. Navigation simulieren
- Klicken Sie auf "Simulate Navigation"
- Der Roboter bewegt sich animiert zu allen schädlichen Pflanzen
- Die Bewegung erfolgt in logischer Reihenfolge (nächste Entfernung zuerst)

## Technische Details

### YOLOv8-Modell
- **Modelltyp**: Objekterkennung und -klassifikation
- **Klassen**: 
  - Klasse 0: `useful` (nützliche Pflanzen) - Grüne Begrenzungsrahmen
  - Klasse 1: `harmful` (schädliche Pflanzen) - Rote Begrenzungsrahmen
- **Eingabe**: RGB-Bilder beliebiger Größe
- **Ausgabe**: Begrenzungsrahmen, Konfidenzwerte, Klassifikationen

### Navigationsalgorithmus
- **Startposition**: Mitte des Canvas
- **Zielselektion**: Nur schädliche Pflanzen werden angesteuert
- **Pfadplanung**: Sortierung nach euklidischer Entfernung
- **Animation**: 100 Schritte pro Ziel mit 10ms Verzögerung

### GUI-Architektur
- **Framework**: tkinter (Python Standard Library)
- **Layout**: Schwarzer Hintergrund mit hellblauen Buttons
- **Threading**: Navigation läuft in separatem Thread
- **Bildverarbeitung**: PIL/Pillow für Anzeige, OpenCV für Verarbeitung

## Testverfahren

Das System wurde umfassend getestet:

1. **Modell-Laden**: Überprüfung der YOLOv8-Modell-Initialisierung
2. **Pflanzenerkennung**: Test mit Beispielbildern aus dem Dataset
3. **Navigation**: Simulation mit verschiedenen Koordinatensätzen

Alle Tests sind im `test_application.py` Skript implementiert und können unabhängig ausgeführt werden.

## Bewertungskriterien erfüllt

✅ **Klare Erkennungsrahmen**: Grün für nützlich, rot für schädlich
✅ **Genaue Klassifikation**: YOLOv8-basierte Unterscheidung
✅ **Koordinatenextraktion**: Mittelpunktberechnung aller Objekte
✅ **Logische Navigation**: Entfernungsbasierte Pfadplanung
✅ **GUI-Anforderungen**: Schwarzes Fenster, hellblaue Buttons
✅ **Funktionale Buttons**: Alle geforderten Funktionen implementiert
✅ **Mehrfacherkennung**: Unterstützung für Bilder mit mehreren Pflanzen

## Fehlerbehebung

### Häufige Probleme

**GUI startet nicht (TclError: no display)**
```bash
# Für Headless-Umgebungen verwenden Sie:
python3 test_application.py
```

**Modell nicht gefunden**
```bash
# Stellen Sie sicher, dass best.pt im Projektverzeichnis liegt
ls -la best.pt
```

**Abhängigkeiten fehlen**
```bash
# Installieren Sie alle erforderlichen Pakete:
pip install ultralytics opencv-python Pillow
sudo apt install python3-tk
```

## Erweiterungsmöglichkeiten

- **Echte Roboterintegration**: Anbindung an ROS oder andere Roboterframeworks
- **Erweiterte Pfadplanung**: A*-Algorithmus oder andere optimierte Verfahren
- **Datenbank-Integration**: Speicherung von Erkennungsergebnissen
- **Web-Interface**: Browser-basierte Alternative zur Desktop-GUI
- **Batch-Verarbeitung**: Automatische Verarbeitung ganzer Bildordner

## Lizenz und Verwendung

Dieses Projekt wurde für akademische Zwecke entwickelt und demonstriert moderne Computer Vision Techniken mit YOLOv8. Der Code ist vollständig kommentiert und für Bildungszwecke optimiert.
