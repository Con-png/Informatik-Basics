import json
import os

# ==========================================================
# HILFSFUNKTIONEN FÜR GEODATEN & ENTFERNUNG
# ==========================================================

### Extraktion des Breitengrades aus einem XML-String
def parse_latitude(trkpt_str:str) -> float:
    # Sucht nach 'lat', splittet beim folgenden Anführungszeichen und extrahiert die Zahl
    return float(trkpt_str.split("lat")[1].split('"')[1])

### Extraktion des Längengrades aus einem XML-String
def parse_longitude(trkpt_str:str) -> float:
    # Sucht nach 'lon', splittet beim folgenden Anführungszeichen und extrahiert die Zahl
    return float(trkpt_str.split("lon")[1].split('"')[1])

### Berechnung der Distanz in Metern zwischen zwei Koordinaten
def distance(pos1:tuple[float,float], pos2:tuple[float,float]) -> float:
    # Umrechnung von Grad-Differenz in Meter (vereinfachte Projektion)
    dlat = 111000 * (pos1[0]-pos2[0]) # 1 Grad Breite = 111km
    dlon = 75000 * (pos1[1]-pos2[1])  # 1 Grad Länge (Mitteleuropa) = 75km
    # Hypotenuse berechnen (Satz des Pythagoras)
    return (dlat ** 2 + dlon ** 2) ** 0.5

### Prüfung, ob zwei Punkte innerhalb eines Radius liegen
def is_close(pos1:tuple[float,float], pos2:tuple[float,float], treshold_m:float = 50) -> bool:
    # Gibt True zurück, wenn die berechnete Distanz unter dem Schwellenwert (50m) liegt
    return distance(pos1,pos2) <= treshold_m 

# ==========================================================
# KLASSE ZUR VERWALTUNG DER POI-DATENBANK (JSON)
# ==========================================================

class POI_Manager:
    __file : str # Pfad zur JSON-Datei

    ### Initialisierung der Klasse mit dem Dateipfad
    def __init__(self, filename:str):
        self.__file = filename

    ### Intern: Daten aus der JSON-Datei laden
    def __get_data(self) -> list[dict]:
        with open(self.__file, encoding="utf-8") as f:
            return json.load(f)
    
    ### Intern: Aktuelle Datenliste dauerhaft in JSON speichern
    def __persist_data(self, data:list[dict]) -> None:
        with open(self.__file, "w", encoding="utf-8") as f:
            return json.dump(data, f, ensure_ascii=False, indent=4)
    
    ### Intern: Suche nach einem POI-Objekt anhand des exakten Namens
    def __get_poi_by_name(self, name:str) -> dict|None:
        for poi in self.__get_data():
            if poi["name"] == name:
                return poi
        return None
    
    ### Anzahl aller gespeicherten POIs ermitteln
    def get_poi_count(self) -> int:
        return len(self.__get_data())
    
    ### Alle vorhandenen POI-Namen als Menge (Set) abrufen
    def get_pois(self) -> set[str]:
        return {poi["name"] for poi in self.__get_data()}
    
    ### Die Koordinaten eines bestimmten POI abfragen
    def get_pos(self, name:str) -> tuple[float,float]|None:
        poi = self.__get_poi_by_name(name)
        return (poi["pos"]["lat"], poi["pos"]["lon"]) if poi is not None else None

    ### Einen neuen POI zur JSON-Liste hinzufügen
    def add_new_poi(self, name:str, pos:tuple[float,float]) -> None:
        # Bestehende Daten laden, neuen Eintrag anhängen und speichern
        self.__persist_data(self.__get_data() + [{
            "name" : name,
            "pos" : {"lat" : pos[0], "lon" : pos[1]}
        }])
    
    ### Finden aller POIs, die sich im Umkreis einer Koordinate befinden
    def get_close_pois(self, pos:tuple[float]) -> set[str]:
        return { poi["name"]
            for poi in self.__get_data()
            if is_close(pos, (poi["pos"]["lat"],poi["pos"]["lon"]))
        }

    ### Die Anzahl der Besuche für einen POI auslesen (und Feld ggf. erstellen)
    def get_visits(self, name:str) -> int|None:
        data = self.__get_data()
        for poi in data:
            if poi["name"] == name:
                if "visits" in poi:
                    return poi["visits"]
                else:
                    # Falls das Feld 'visits' in der JSON noch fehlt, mit 0 anlegen
                    poi["visits"] = 0
                    self.__persist_data(data)
                    return 0
        return None    

    ### Den Besuchszähler eines POI um 1 erhöhen
    def _add_visit(self, name:str) -> None:
        data = self.__get_data()
        for poi in data:
            if poi["name"] == name:
                if "visits" not in poi:
                    poi["visits"] = 0
                poi["visits"] += 1
                self.__persist_data(data)
                return

    ### Die Top-Liste der meistbesuchten POIs erstellen
    def top_visits(self, count:int = 5) -> list[str]:
        data = self.__get_data()
        # Sortiert die Liste absteigend nach dem Wert im Feld 'visits'
        data.sort(key = lambda poi: poi.get("visits", 0), reverse=True)
        return [poi["name"] for poi in data[:count]]
    
    ### Eine GPX-Datei einlesen und Besuche für passierte POIs registrieren
    def process_gpx(self, filepath:str) -> set[str]:
        visited_in_this_track = set() # Verhindert, dass ein POI pro Datei mehrfach zählt
        with open(filepath) as f:
            for line in f:
                # Wir suchen nur Zeilen, die einen Trackpoint (<trkpt) enthalten
                if "<trkpt" in line:
                    lat = parse_latitude(line)
                    lon = parse_longitude(line)
                    # Prüfen, ob dieser Punkt nah an gespeicherten POIs liegt
                    pois = self.get_close_pois((lat,lon))
                    for poi in pois:
                        if poi not in visited_in_this_track:
                            visited_in_this_track.add(poi)
                            self._add_visit(poi) # Zähler in der JSON-Datei erhöhen
        return visited_in_this_track

# ==========================================================
# HAUPTPROGRAMM (BENUTZEROBERFLÄCHE)
# ==========================================================

if __name__ == "__main__":
    manager = POI_Manager("../poi.json")
    
    while True:
        selection = input("""
            --- POI Manager Menü ---
            1) POI suchen
            2) POI hinzufügen
            3) Top 5 POIs anzeigen
            4) GPX-Dateien aus Ordner einlesen
            5) Beenden
            Auswahl: """)

        match selection.strip():
            case "1": # Suche
                substr = input("Name des gesuchten POI: ")
                for poi in manager.get_pois():
                    if substr.lower() in poi.lower():
                        print(f" - {poi} {manager.get_pos(poi)}")
            
            case "2": # Neu anlegen
                name = input("Name des neuen POI: ")
                pos_raw = input("Koordinaten (lat,lon): ")
                pos = tuple(float(p) for p in pos_raw.split(","))
                
                # Prüfen, ob am selben Ort schon POIs existieren
                close_pois = manager.get_close_pois(pos)
                if close_pois:
                    ans = input(f"Achtung, folgende POIs sind bereits nah dran: {','.join(close_pois)}\nTrotzdem speichern? (yes/no): ")
                    if "yes" not in ans.lower():
                        continue
                manager.add_new_poi(name, pos)
                print(f"POI '{name}' wurde hinzugefügt.")

            case "3": # Statistik
                top = manager.top_visits()
                print("\nUnsere Top-Ziele:")
                for i, name in enumerate(top):
                    print(f"{i+1}. {name} {manager.get_pos(name)} - {manager.get_visits(name)} Besuche")

            case "4": # GPX-Verarbeitung
                dirpath = input("Pfad zum Ordner mit GPX-Dateien: ")
                if os.path.exists(dirpath):
                    for file in os.listdir(dirpath):
                        if file.endswith(".gpx"):
                            print(f" - Verarbeite {file}... ", end="")
                            found = manager.process_gpx(os.path.join(dirpath, file))
                            print(f"Besucht: {', '.join(found) if found else 'Keine POIs gefunden'}")
                else:
                    print("Pfad nicht gefunden!")

            case "5": # Beenden
                print("Programm wird beendet. Auf Wiedersehen!")
                break
