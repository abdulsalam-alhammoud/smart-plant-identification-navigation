import cv2
from ultralytics import YOLO

class PlantDetector:
    def __init__(self, model_path='best.pt'):
        # Modell laden
        # Lädt ein vortrainiertes YOLOv8-Modell von dem angegebenen Pfad.
        self.model = YOLO(model_path)
        # Klassen-Mapping
        # Definiert, welche Klassen als 'nützlich' (grün) und 'schädlich' (rot) eingestuft werden.
        self.class_names = {
            0: 'useful',
            1: 'harmful'
        }

    def detect(self, image_path):
        # Bild laden
        # Lädt das Bild von dem angegebenen Pfad.
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Bild nicht gefunden unter: {image_path}")

        # Vorhersagen durchführen
        # Führt Objekterkennung auf dem geladenen Bild durch.
        results = self.model(img)

        detections = []
        # Ergebnisse verarbeiten
        # Iteriert durch die erkannten Objekte und extrahiert deren Informationen.
        for r in results:
            for *xyxy, conf, cls in r.boxes.data:
                x1, y1, x2, y2 = map(int, xyxy)
                class_id = int(cls)
                class_name = self.class_names.get(class_id, 'unknown')

                # Mittelpunkt berechnen
                # Berechnet die X- und Y-Koordinaten des Mittelpunkts des Begrenzungsrahmens.
                x_center = (x1 + x2) // 2
                y_center = (y1 + y2) // 2

                detections.append({
                    'box': [x1, y1, x2, y2],
                    'confidence': float(conf),
                    'class_id': class_id,
                    'class_name': class_name,
                    'center_coordinates': (x_center, y_center)
                })
        return img, detections

    def draw_boxes(self, img, detections):
        # Begrenzungsrahmen zeichnen
        # Zeichnet Begrenzungsrahmen und Beschriftungen auf das Bild.
        for det in detections:
            x1, y1, x2, y2 = det['box']
            class_name = det['class_name']
            x_center, y_center = det['center_coordinates']

            color = (0, 255, 0) if class_name == 'useful' else (0, 0, 255)  # Grün für nützlich, Rot für schädlich
            label = f"{class_name}: {det['confidence']:.2f}"

            # Rechteck zeichnen
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            # Text für Beschriftung zeichnen
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # Mittelpunkt zeichnen
            cv2.circle(img, (x_center, y_center), 5, color, -1)
        return img

if __name__ == '__main__':
    detector = PlantDetector()
    # Beispielbild für Tests
    # Stellen Sie sicher, dass ein Bild 'test_image.jpg' im selben Verzeichnis existiert oder geben Sie den vollständigen Pfad an.
    test_image_path = 'cwfid_001_image.png'
    try:
        original_img, detected_plants = detector.detect(test_image_path)
        if detected_plants:
            print("Erkannte Pflanzen:")
            for plant in detected_plants:
                print(f"  Klasse: {plant['class_name']}, Konfidenz: {plant['confidence']:.2f}, Koordinaten: {plant['center_coordinates']}")
            img_with_boxes = detector.draw_boxes(original_img.copy(), detected_plants)
            cv2.imwrite('detected_image.jpg', img_with_boxes)
            print("Bild mit Begrenzungsrahmen gespeichert als 'detected_image.jpg'")
        else:
            print("Keine Pflanzen im Bild erkannt.")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

