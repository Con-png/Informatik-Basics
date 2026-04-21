# Depends on 03

"""

Implement two new methods for `POI_Manager` that lets you manage how many times a POI was visited:

def _get_visits(self, name:str) -> int|None
def _add_visit(self, name:str) -> None

The first returns, how many times a POI was visited in the past. If no such data is recorded for a POI yet, it returns 0, 
and initializes that data in the json file. If no POI with that name exists, the function returns None.

The second funtion increases that data by 1, or sets it to 1 if the data did not exist yet. 

"""

# Copy-paste your class defition here from 03 (or 06) and extend it with the new methods

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

    def _get_visits(self, name: str) -> int | None: 
        data = self._load_data()
        poi_found = None

        # 1. Den richtigen POI in der Liste suchen
        for item in data:
            if item['name'].lower() == name.lower():
                poi_found = item
                break

        # Falls der Name nicht gefunden wurde
        if poi_found is None:
            return None

        # 2. Prüfen, ob 'visits' existiert
        if 'visits' not in poi_found:
            # Initialisieren, falls das Feld fehlt
            poi_found['visits'] = 0
            
            # Die Änderung muss in die JSON-Datei geschrieben werden!
            with open(self.file_path, 'w', encoding='utf-8') as datei:
                json.dump(data, datei, indent=4, ensure_ascii=False)
            
            return 0
        
        # 3. Den vorhandenen Wert zurückgeben
        return poi_found['visits']
    
    def _add_visit(self, name: str) -> None:
        data = self._load_data()
        poi_found = None

        # 1. POI suchen
        for item in data:
            if item['name'].lower() == name.lower():
                poi_found = item
                break

        # 2. Nur wenn der POI existiert, Daten ändern und speichern
        if poi_found is not None:
            if 'visits' in poi_found:
                poi_found['visits'] += 1  # Erhöhen
            else:
                poi_found['visits'] = 1   # Neu setzen auf 1
            
            # Direktes Speichern in dieser Methode
            with open(self.file_path, 'w', encoding='utf-8') as datei:
                json.dump(data, datei, indent=4, ensure_ascii=False)


# Tests 

import unittest
class Test_POI_Manager_4(unittest.TestCase):

    def test_get_visits(self):
        pass

    def test_add_visits(self):
        pass

if __name__ == '__main__':
    unittest.main()


