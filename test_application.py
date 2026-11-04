#!/usr/bin/env python3
"""
Smart Plant Identification and Navigation Tool - Test Script
Dieses Skript testet die Funktionalität ohne GUI für Headless-Umgebungen.
"""

import cv2
import os
from detector import PlantDetector
from navigator import RobotNavigator

def test_detection():
    """Testet die Pflanzenerkennung."""                          
    print("=== Test der Pflanzenerkennung ===")
    
    detector = PlantDetector()
    test_image = 'cwfid_001_image.png'
    
    if not os.path.exists(test_image):
        print(f"Testbild {test_image} nicht gefunden!")
        return False
    
    try:
        # Erkennung durchführen
        original_img, detections = detector.detect(test_image)
        
        print(f"Erkannte Pflanzen: {len(detections)}")
        
        if detections:
            # Statistiken
            useful_count = sum(1 for d in detections if d['class_name'] == 'useful')
            harmful_count = sum(1 for d in detections if d['class_name'] == 'harmful')
            
            print(f"  - Nützliche Pflanzen: {useful_count}")
            print(f"  - Schädliche Pflanzen: {harmful_count}")
            
            # Bild mit Begrenzungsrahmen speichern
            img_with_boxes = detector.draw_boxes(original_img.copy(), detections)
            output_path = 'test_detection_result.jpg'
            cv2.imwrite(output_path, img_with_boxes)
            print(f"  - Ergebnis gespeichert als: {output_path}")
            
            # Koordinaten ausgeben
            print("\nKoordinaten der erkannten Pflanzen:")
            for i, det in enumerate(detections, 1):
                x, y = det['center_coordinates']
                print(f"  {i}. {det['class_name'].capitalize()} bei ({x}, {y}) - Konfidenz: {det['confidence']:.2f}")
            
            return True
        else:
            print("Keine Pflanzen erkannt.")
            return False
            
    except Exception as e:
        print(f"Fehler bei der Erkennung: {e}")
        return False

def test_navigation():
    """Testet die Navigationslogik."""
    print("\n=== Test der Navigation ===")
    
    # Beispielkoordinaten von schädlichen Pflanzen
    harmful_plants = [(100, 150), (300, 200), (500, 100), (200, 400)]
    
    def dummy_update_gui(x, y):
        print(f"  Roboter Position: ({x}, {y})")
    
    navigator = RobotNavigator(canvas_width=600, canvas_height=500)
    
    print(f"Simuliere Navigation zu {len(harmful_plants)} schädlichen Pflanzen...")
    print("Roboter Startposition:", navigator.robot_position)
    
    try:
        navigator.simulate_movement(harmful_plants, dummy_update_gui)
        print("Navigation erfolgreich abgeschlossen!")
        return True
    except Exception as e:
        print(f"Fehler bei der Navigation: {e}")
        return False

def test_model_loading():
    """Testet das Laden des YOLOv8-Modells."""
    print("=== Test des Modell-Ladens ===")
    
    model_path = 'best.pt'
    if not os.path.exists(model_path):
        print(f"Modell {model_path} nicht gefunden!")
        return False
    
    try:
        detector = PlantDetector(model_path)
        print("YOLOv8-Modell erfolgreich geladen!")
        print(f"Modell-Pfad: {model_path}")
        return True
    except Exception as e:
        print(f"Fehler beim Laden des Modells: {e}")
        return False

def main():
    """Hauptfunktion für alle Tests."""
    print("Smart Plant Identification and Navigation Tool - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Modell-Laden", test_model_loading),
        ("Pflanzenerkennung", test_detection),
        ("Navigation", test_navigation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\nStarte Test: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print(f"Test {test_name}: {'BESTANDEN' if result else 'FEHLGESCHLAGEN'}")
    
    print("\n" + "=" * 60)
    print("TESTERGEBNISSE:")
    for test_name, result in results:
        status = "✓ BESTANDEN" if result else "✗ FEHLGESCHLAGEN"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nGesamtergebnis: {'ALLE TESTS BESTANDEN' if all_passed else 'EINIGE TESTS FEHLGESCHLAGEN'}")
    
    if all_passed:
        print("\nDie Anwendung ist bereit für den Einsatz!")
        print("Starten Sie die GUI mit: python3 main_gui.py")
    else:
        print("\nBitte beheben Sie die Fehler vor dem Einsatz der Anwendung.")

if __name__ == "__main__":
    main()
