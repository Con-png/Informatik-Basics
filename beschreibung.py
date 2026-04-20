# 📍 GPS & POI Analytics Engine

Dieses Projekt stellt ein modulares Framework zur Verwaltung von Points of Interest (POIs) und zur automatisierten Analyse von GPX-Bewegungsdaten bereit.

## 📑 Inhaltsverzeichnis
1. [Geo-Utilities](#1-geo-utilities)
2. [Persistence Layer](#2-persistence-layer)
3. [POI Management](#3-poi-management)
4. [Visit Analytics](#4-visit-analytics)
5. [GPX Processing Engine](#5-gpx-processing-engine)
6. [CLI-Interface](#6-cli-interface)

---

### 1. Geo-Utilities
**Beschreibung:** Extraktion von Rohdaten und mathematische Distanzberechnung.

```python
# Extraktion von Breitengrad aus XML-Attributen
def parse_latitude(trkpt_str: str) -> float:
    return float(trkpt_str.split("lat")[1].split('"')[1])

# Extraktion von Längengrad aus XML-Attributen
def parse_longitude(trkpt_str: str) -> float:
    return float(trkpt_str.split("lon")[1].split('"')[1])

# Euklidische Distanzberechnung in Metern
def distance(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    dlat = 111000 * (pos1[0] - pos2[0])
    dlon = 75000 * (pos1[1] - pos2[1])
    return (dlat**2 + dlon**2)**0.5

# Radius-Validierung (Geofencing)
def is_close(pos1: tuple[float, float], pos2: tuple[float, float], threshold_m: float = 50) -> bool:
    return distance(pos1, pos2) <= threshold_m
