import json
import os
import math

script_dir = os.path.dirname(__file__)

class POI_Manager:
    def __init__(self, poi_dateiname):
        self.file_path = os.path.join(script_dir, poi_dateiname)
        # Ensure file exists to prevent errors
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _load_data(self) -> list:
        """Helper method to load the JSON content."""
        try:
            with open(self.file_path, 'r', encoding="utf-8") as datei:
                return json.load(datei)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def get_poi_count(self) -> int:
        return len(self._load_data())

    def get_pois(self) -> set[str]:
        data = self._load_data()
        return {item['name'] for item in data}

    def get_pos(self, name: str) -> tuple[float, float] | None:
        data = self._load_data()
        for item in data:
            if item['name'].lower() == name.lower():
                return (item['pos']['lat'], item['pos']['lon'])
        return None

    def search_pois(self, search_string: str):
        data = self._load_data()
        search_string = search_string.lower()
        return [item for item in data if search_string in item['name'].lower()]

    def calculate_distance(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
        """Calculates distance between two points in km using Haversine formula."""
        lat1, lon1 = map(math.radians, pos1)
        lat2, lon2 = map(math.radians, pos2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c  # Radius of Earth in kilometers

    def find_nearby_poi(self, pos: tuple[float, float], threshold_km: float = 0.2):
        """Returns the name of a POI if it's within the threshold distance."""
        data = self._load_data()
        for item in data:
            existing_pos = (item['pos']['lat'], item['pos']['lon'])
            if self.calculate_distance(pos, existing_pos) < threshold_km:
                return item['name']
        return None

    def add_new_poi(self, name: str, pos: tuple[float, float]) -> None:
        """Adds a new POI to the JSON data."""
        data = self._load_data()
        new_poi = {
            "name": name,
            "pos": {
                "lat": pos[0],
                "lon": pos[1]
            }
        }
        data.append(new_poi)
        with open(self.file_path, 'w', encoding='utf-8') as datei:
            json.dump(data, datei, indent=4, ensure_ascii=False)

# --- Menu Logic ---

poim = POI_Manager("poi_test.json")

while True:
    print("""
--- POI Manager ---
 1) Search for a POI
 2) Add new POI
 3) TOP 5 most popular POIs
 4) Add visits from GPX file
 5) Exit""")
    
    entscheidung = input("Welche Entscheidung? ")

    if entscheidung == "1":
        ort = input("Welcher POI-Name? ")
        pos = poim.get_pos(ort)
        if pos:
            print(f"Gefunden: {ort} bei {pos}")
        else:
            print("POI nicht gefunden.")

    elif entscheidung == "2":
        name = input("Wie heißt der Ort? ")
        try:
            lat = float(input("Lat? "))
            lon = float(input("Lon? "))
            new_pos = (lat, lon)

            # BONUS: Proximity Check
            nearby_name = poim.find_nearby_poi(new_pos, threshold_km=0.1) # 100 meters
            
            proceed = "y"
            if nearby_name:
                print(f"WARNUNG: Der POI '{nearby_name}' ist bereits ganz in der Nähe.")
                proceed = input("Möchten Sie diesen trotzdem hinzufügen? (y/n): ").lower()

            if proceed == "y":
                poim.add_new_poi(name, new_pos)
                print(f"'{name}' wurde erfolgreich hinzugefügt.")
            else:
                print("Abgebrochen.")
                
        except ValueError:
            print("Fehler: Bitte geben Sie gültige Zahlen für die Koordinaten ein.")

    elif entscheidung == "5":
        print("Auf Wiedersehen!")
        break
    else:
        print("Diese Funktion ist noch nicht verfügbar oder die Eingabe war ungültig.")