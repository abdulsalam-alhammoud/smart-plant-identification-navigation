import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import cv2
import threading
from detector import PlantDetector
from navigator import RobotNavigator

class PlantRobotGUI:
    def __init__(self, root):
        # Initialisiert die GUI-Anwendung.
        self.root = root
        self.root.title("Smart Plant Identification and Navigation Tool")
        self.root.configure(bg='black')
        self.root.geometry("1200x800")

        # Initialisiert die Komponenten
        self.detector = PlantDetector()
        self.navigator = None
        self.current_image = None
        self.current_detections = []
        self.image_path = None

        # GUI-Elemente erstellen
        self.create_widgets()

    def create_widgets(self):
        # Erstellt alle GUI-Elemente.
        
        # Hauptframe
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Linke Seite: Buttons
        button_frame = tk.Frame(main_frame, bg='black', width=200)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        button_frame.pack_propagate(False)

        # Buttons mit hellblauer Farbe
        button_color = '#87CEEB'  # Hellblau
        button_font = ('Arial', 12, 'bold')

        self.upload_btn = tk.Button(button_frame, text="Upload Image", 
                                   command=self.upload_image, 
                                   bg=button_color, font=button_font, 
                                   width=15, height=2)
        self.upload_btn.pack(pady=10)

        self.detect_btn = tk.Button(button_frame, text="Run Detection", 
                                   command=self.run_detection, 
                                   bg=button_color, font=button_font, 
                                   width=15, height=2, state=tk.DISABLED)
        self.detect_btn.pack(pady=10)

        self.coordinates_btn = tk.Button(button_frame, text="Show Coordinates", 
                                        command=self.show_coordinates, 
                                        bg=button_color, font=button_font, 
                                        width=15, height=2, state=tk.DISABLED)
        self.coordinates_btn.pack(pady=10)

        self.navigate_btn = tk.Button(button_frame, text="Simulate Navigation", 
                                     command=self.simulate_navigation, 
                                     bg=button_color, font=button_font, 
                                     width=15, height=2, state=tk.DISABLED)
        self.navigate_btn.pack(pady=10)

        self.exit_btn = tk.Button(button_frame, text="Exit", 
                                 command=self.root.quit, 
                                 bg=button_color, font=button_font, 
                                 width=15, height=2)
        self.exit_btn.pack(pady=10)

        # Rechte Seite: Bildanzeige und Informationen
        content_frame = tk.Frame(main_frame, bg='black')
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Bildanzeige
        self.image_label = tk.Label(content_frame, bg='black', text="Kein Bild geladen", 
                                   fg='white', font=('Arial', 14))
        self.image_label.pack(pady=10)

        # Informationsbereich
        info_frame = tk.Frame(content_frame, bg='black')
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(info_frame, text="Informationen:", bg='black', fg='white', 
                font=('Arial', 12, 'bold')).pack(anchor=tk.W)

        self.info_text = scrolledtext.ScrolledText(info_frame, height=10, 
                                                  bg='white', fg='black', 
                                                  font=('Arial', 10))
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Canvas für Navigation
        self.canvas = tk.Canvas(content_frame, bg='white', height=200)
        self.canvas.pack(fill=tk.X, pady=10)

    def upload_image(self):
        # Lädt ein Bild hoch.
        file_path = filedialog.askopenfilename(
            title="Bild auswählen",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            self.detect_btn.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Bild geladen: {file_path}\n")

    def display_image(self, image_path):
        # Zeigt das Bild in der GUI an.
        try:
            # Bild laden und skalieren
            image = Image.open(image_path)
            # Maximale Größe für die Anzeige
            max_width, max_height = 600, 400
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo  # Referenz behalten
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden des Bildes: {e}")

    def run_detection(self):
        # Führt die Pflanzenerkennung durch.
        if not self.image_path:
            messagebox.showwarning("Warnung", "Bitte laden Sie zuerst ein Bild hoch.")
            return

        try:
            self.info_text.insert(tk.END, "Führe Erkennung durch...\n")
            self.root.update()

            # Erkennung durchführen
            original_img, detections = self.detector.detect(self.image_path)
            self.current_image = original_img
            self.current_detections = detections

            if detections:
                # Bild mit Begrenzungsrahmen zeichnen
                img_with_boxes = self.detector.draw_boxes(original_img.copy(), detections)
                
                # Temporäres Bild speichern und anzeigen
                temp_path = "temp_detection.jpg"
                cv2.imwrite(temp_path, img_with_boxes)
                self.display_image(temp_path)

                # Ergebnisse anzeigen
                self.info_text.insert(tk.END, f"Erkennung abgeschlossen! {len(detections)} Pflanzen erkannt.\n")
                
                # Buttons aktivieren
                self.coordinates_btn.config(state=tk.NORMAL)
                self.navigate_btn.config(state=tk.NORMAL)
            else:
                self.info_text.insert(tk.END, "Keine Pflanzen im Bild erkannt.\n")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Erkennung: {e}")

    def show_coordinates(self):
        # Zeigt die Koordinaten der erkannten Pflanzen an.
        if not self.current_detections:
            messagebox.showwarning("Warnung", "Keine Erkennungen verfügbar.")
            return

        self.info_text.insert(tk.END, "\n--- Koordinaten der erkannten Pflanzen ---\n")
        
        for i, detection in enumerate(self.current_detections, 1):
            class_name = detection['class_name']
            confidence = detection['confidence']
            x_center, y_center = detection['center_coordinates']
            
            self.info_text.insert(tk.END, 
                f"{i}. {class_name.capitalize()} (Konfidenz: {confidence:.2f}) - "
                f"Koordinaten: ({x_center}, {y_center})\n")

    def simulate_navigation(self):
        # Simuliert die Roboternavigation.
        if not self.current_detections:
            messagebox.showwarning("Warnung", "Keine Erkennungen verfügbar.")
            return

        # Schädliche Pflanzen filtern
        harmful_plants = [det for det in self.current_detections if det['class_name'] == 'harmful']
        
        if not harmful_plants:
            messagebox.showinfo("Information", "Keine schädlichen Pflanzen für die Navigation gefunden.")
            return

        # Canvas vorbereiten
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:  # Canvas noch nicht gerendert
            canvas_width = 800
            canvas_height = 200

        # Navigator initialisieren
        self.navigator = RobotNavigator(canvas_width, canvas_height)

        # Koordinaten für Canvas skalieren
        if self.current_image is not None:
            img_height, img_width = self.current_image.shape[:2]
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
        else:
            scale_x = scale_y = 1

        scaled_coordinates = []
        for plant in harmful_plants:
            x, y = plant['center_coordinates']
            scaled_x = int(x * scale_x)
            scaled_y = int(y * scale_y)
            scaled_coordinates.append((scaled_x, scaled_y))
            # Schädliche Pflanzen als rote Kreise zeichnen
            self.canvas.create_oval(scaled_x-5, scaled_y-5, scaled_x+5, scaled_y+5, 
                                   fill='red', outline='darkred')

        self.info_text.insert(tk.END, f"\nStarte Navigation zu {len(harmful_plants)} schädlichen Pflanzen...\n")

        # Navigation in separatem Thread starten
        def navigation_thread():
            self.navigator.simulate_movement(scaled_coordinates, self.update_robot_position)

        threading.Thread(target=navigation_thread, daemon=True).start()

    def update_robot_position(self, x, y):
        # Aktualisiert die Roboterposition auf dem Canvas.
        self.root.after(0, self._draw_robot, x, y)

    def _draw_robot(self, x, y):
        # Zeichnet den Roboter auf dem Canvas.
        self.canvas.delete("robot")
        self.canvas.create_oval(x-8, y-8, x+8, y+8, fill='blue', outline='darkblue', tags="robot")
        self.canvas.create_text(x, y-15, text="Robot", fill='blue', tags="robot")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlantRobotGUI(root)
    root.mainloop()
