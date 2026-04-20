

GPS & POI Analytics Engine

Dieses Projekt stellt ein modulares Framework zur Verwaltung von Points of Interest (POIs) und zur automatisierten Analyse von GPX-Bewegungsdaten bereit. 
Es ermöglicht den Abgleich von GPS-Koordinaten mit einer lokalen Datenbank, um Besuchsstatistiken basierend auf räumlicher Nähe zu führen.

## 📑 Inhaltsverzeichnis

1.  [Geo-Utilities (Parsing & Geometrie)](https://www.google.com/search?q=%231-geo-utilities)
2.  [Persistence Layer (Datenhaltung)](https://www.google.com/search?q=%232-persistence-layer)
3.  [POI Management (Kernfunktionen)](https://www.google.com/search?q=%233-poi-management)
4.  [Visit Analytics (Statistik)](https://www.google.com/search?q=%234-visit-analytics)
5.  [GPX Processing Engine (Analyse)](https://www.google.com/search?q=%235-gpx-processing-engine)
6.  [CLI-Interface (Steuerung)](https://www.google.com/search?q=%236-cli-interface)

-----

### 1\. Geo-Utilities

**Beschreibung:** Dieser Layer ist für die Rohdaten-Extraktion und die mathematische Distanzberechnung zuständig. Er wandelt XML-Strings in numerische Werte um und prüft räumliche Beziehungen.

```python
# Extraktion von Breitengrad aus XML-Attributen
def parse_latitude(trkpt_str: str) -> float:
    return float(trkpt_str.split("lat")[1].split('"')[1])

# Extraktion von Längengrad aus XML-Attributen
def parse_longitude(trkpt_str: str) -> float:
    return float(trkpt_str.split("lon")[1].split('"')[1])

# Euklidische Distanzberechnung in Metern (Annäherung)
def distance(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    dlat = 111000 * (pos1[0] - pos2[0])
    dlon = 75000 * (pos1[1] - pos2[1])
    return (dlat**2 + dlon**2)**0.5

# Radius-Validierung (Geofencing)
def is_close(pos1: tuple[float, float], pos2: tuple[float, float], threshold_m: float = 50) -> bool:
    return distance(pos1, pos2) <= threshold_m
```

-----

### 2\. Persistence Layer

**Beschreibung:** Verantwortlich für die Serialisierung und Deserialisierung der Daten. Er stellt sicher, dass alle Änderungen (neue POIs oder Besuche) permanent in der JSON-Datenbank gespeichert werden.

```python
import json

# Datenbank-Read (Deserialisierung)
def __get_data(self) -> list[dict]:
    with open(self.__file, encoding="utf-8") as f:
        return json.load(f)

# Datenbank-Write (Serialisierung)
def __persist_data(self, data: list[dict]) -> None:
    with open(self.__file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
```

-----

### 3\. POI Management

**Beschreibung:** Beinhaltet die Kernlogik zur Verwaltung der POI-Objekte. Dazu gehört das Anlegen neuer Datensätze sowie die räumliche Suche nach Treffern in der Datenbank.

```python
# Initialisierung neuer POIs mit Basis-Attributen
def add_new_poi(self, name: str, pos: tuple[float, float]) -> None:
    data = self.__get_data()
    data.append({
        "name": name,
        "pos": {"lat": pos[0], "lon": pos[1]},
        "visits": 0
    })
    self.__persist_data(data)

# Räumlicher Filter zur Identifikation von Treffern im Umkreis
def get_close_pois(self, pos: tuple[float, float]) -> set[str]:
    return { poi["name"] for poi in self.__get_data() 
             if is_close(pos, (poi["pos"]["lat"], poi["pos"]["lon"])) }
```

-----

### 4\. Visit Analytics

**Beschreibung:** Verarbeitet Nutzungsmetriken. Dieser Teil aggregiert Besuche und stellt Funktionen bereit, um Popularitäts-Rankings (Top-Listen) aus der Datenbank zu generieren.

```python
# Inkrementelle Aktualisierung der Besuchszahlen pro POI
def _add_visit(self, name: str) -> None:
    data = self.__get_data()
    for poi in data:
        if poi["name"] == name:
            poi["visits"] = poi.get("visits", 0) + 1
            self.__persist_data(data)
            return

# Generierung einer Bestenliste (Descending Sort via Lambda)
def top_visits(self, count: int = 5) -> list[str]:
    data = self.__get_data()
    data.sort(key=lambda poi: poi.get("visits", 0), reverse=True)
    return [poi["name"] for poi in data[:count]]
```

-----

### 5\. GPX Processing Engine

**Beschreibung:** Die Schnittstelle zwischen Dateisystem und Logik. Sie analysiert Track-Dateien sequenziell und führt den Abgleich mit dem POI-Manager durch.

```python
# Analyse von GPX-Dateien inkl. Deduplizierung pro Track
def process_gpx(self, filepath: str) -> set[str]:
    visited_in_track = set() 
    with open(filepath) as f:
        for line in f:
            if "<trkpt" in line:
                pos = (parse_latitude(line), parse_longitude(line))
                matches = self.get_close_pois(pos)
                for poi in matches:
                    if poi not in visited_in_track:
                        visited_in_track.add(poi)
                        self._add_visit(poi)
    return visited_in_track
```

-----

### 6\. CLI-Interface

**Beschreibung:** Das Benutzerinterface zur Steuerung der Applikation. Es implementiert das Command-Routing und ermöglicht die Stapelverarbeitung (Batch Processing) ganzer Verzeichnisse.

```python
import os

# Stapelverarbeitung von Verzeichnissen
def run_batch_processing(dirpath: str):
    if os.path.exists(dirpath):
        for filename in os.listdir(dirpath):
            if filename.endswith(".gpx"):
                path = os.path.join(dirpath, filename)
                visited = manager.process_gpx(path)
                print(f"Track: {filename} verarbeitet. Gefundene POIs: {visited}")

# Command-Routing via Match-Case (Python 3.10+)
match selection.strip():
    case "4":
        path = input("Pfad zu den GPX-Dateien: ")
        run_batch_processing(path)
```
