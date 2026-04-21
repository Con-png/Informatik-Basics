import json
import os
import math

script_dir = os.path.dirname(__file__)

class POI_Manager:
    def __init__(self, poi_dateiname):
        self.file_path = os.path.join(script_dir, poi_dateiname)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def get_poi_count(self) -> int:
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        return len(data)

    def get_pois(self) -> set[str]:
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        return {item['name'] for item in data}

    def get_pos(self, name: str) -> tuple[float, float] | None:
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        for item in data:
            if item['name'].lower() == name.lower():
                return (item['pos']['lat'], item['pos']['lon'])
        return None

    def search_pois(self, search_string: str):
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        search_string = search_string.lower()
        return [item for item in data if search_string in item['name'].lower()]

    def calculate_distance(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
        lat1, lon1 = map(math.radians, pos1)
        lat2, lon2 = map(math.radians, pos2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c

    def find_nearby_poi(self, pos: tuple[float, float], threshold_km: float = 0.2):
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        for item in data:
            existing_pos = (item['pos']['lat'], item['pos']['lon'])
            if self.calculate_distance(pos, existing_pos) < threshold_km:
                return item['name']
        return None

    def add_new_poi(self, name: str, pos: tuple[float, float]) -> None:
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        new_poi = {
            "name": name,
            "pos": {"lat": pos[0], "lon": pos[1]},
            "visits": 0
        }
        data.append(new_poi)
        with open(self.file_path, 'w', encoding='utf-8') as datei:
            json.dump(data, datei, indent=4, ensure_ascii=False)

    def _get_visits(self, name: str) -> int | None: 
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        for item in data:
            if item['name'].lower() == name.lower():
                return item.get('visits', 0)
        return None
    
    def _add_visit(self, name: str) -> None:
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        for item in data:
            if item['name'].lower() == name.lower():
                item['visits'] = item.get('visits', 0) + 1
                with open(self.file_path, 'w', encoding='utf-8') as datei:
                    json.dump(data, datei, indent=4, ensure_ascii=False)
                return

    def get_top_pois(self, limit: int = 5) -> list:
        with open(self.file_path, 'r', encoding="utf-8") as datei:
            data = json.load(datei)
        sorted_data = sorted(data, key=lambda x: x.get('visits', 0), reverse=True)
        return sorted_data[:limit]


# --- Menü Logik ---
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
            besuche = poim._get_visits(ort)
            print(f"Gefunden: {ort} bei {pos} | Besuche: {besuche}")
        else:
            print("POI nicht gefunden.")

    elif entscheidung == "2":
        name = input("Wie heißt der Ort? ")
        try:
            lat = float(input("Lat? "))
            lon = float(input("Lon? "))
            new_pos = (lat, lon)
            nearby_name = poim.find_nearby_poi(new_pos, threshold_km=0.1)
            
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
            print("Fehler: Bitte gültige Zahlen eingeben.")

    elif entscheidung == "3":
        top_list = poim.get_top_pois(5)
        print("\n--- TOP 5 POIs ---")
        if not top_list:
            print("Keine POIs vorhanden.")
        for i, poi in enumerate(top_list, 1):
            v = poi.get('visits', 0)
            print(f"{i}. {poi['name']} ({v} Besuche)")

    elif entscheidung == "5":
        print("Programm beendet.")
        break
    
    else:
        print("Diese Funktion ist noch nicht verfügbar oder die Eingabe war ungültig.")