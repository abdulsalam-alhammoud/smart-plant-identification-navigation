import time

class RobotNavigator:
    def __init__(self, canvas_width, canvas_height):
        # Initialisiert den Navigator mit den Dimensionen des Canvas.
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.robot_position = (canvas_width // 2, canvas_height // 2)  # Startposition des Roboters (Mitte des Canvas)

    def simulate_movement(self, harmful_plants_coordinates, update_gui_callback):
        # Simuliert die Bewegung des Roboters zu schädlichen Pflanzen.
        # harmful_plants_coordinates: Eine Liste von (x, y) Koordinaten der schädlichen Pflanzen.
        # update_gui_callback: Eine Funktion, die aufgerufen wird, um die GUI zu aktualisieren (z.B. Roboterposition zeichnen).

        if not harmful_plants_coordinates:
            print("Keine schädlichen Pflanzen für die Navigation gefunden.")
            return

        # Sortiert die Pflanzen nach ihrer Entfernung zur aktuellen Roboterposition, um eine logische Bewegung zu simulieren.
        # Dies verhindert zufälliges Springen und fördert eine geordnete Abarbeitung.
        sorted_plants = sorted(harmful_plants_coordinates, key=lambda p: self._distance(self.robot_position, p))

        for target_x, target_y in sorted_plants:
            print(f"Navigiere zu schädlicher Pflanze bei: ({target_x}, {target_y})")
            # Bewege den Roboter schrittweise zum Ziel.
            steps = 100  # Anzahl der Schritte für die Animation
            for i in range(steps + 1):
                # Berechnet die aktuelle Position des Roboters auf dem Weg zum Ziel.
                current_x = int(self.robot_position[0] + (target_x - self.robot_position[0]) * i / steps)
                current_y = int(self.robot_position[1] + (target_y - self.robot_position[1]) * i / steps)

                # Aktualisiert die GUI mit der neuen Roboterposition.
                update_gui_callback(current_x, current_y)
                time.sleep(0.01)  # Kleine Pause für die Animation

            self.robot_position = (target_x, target_y)  # Roboter erreicht das Ziel
            print(f"Roboter hat Pflanze bei ({target_x}, {target_y}) erreicht.")

    def _distance(self, p1, p2):
        # Berechnet den euklidischen Abstand zwischen zwei Punkten.
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# Beispielnutzung (für Tests ohne GUI):
if __name__ == '__main__':
    # Dummy-Callback-Funktion für Tests
    def dummy_update_gui(x, y):
        print(f"Roboter bei: ({x}, {y})")

    navigator = RobotNavigator(canvas_width=800, canvas_height=600)
    # Beispielkoordinaten von schädlichen Pflanzen
    harmful_plants = [(100, 100), (700, 500), (400, 200)]
    navigator.simulate_movement(harmful_plants, dummy_update_gui)

