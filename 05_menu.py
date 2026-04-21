# Depends on 03

"""

Write a simple program, that displays a menu like this:

What do you want to do?
 1) Search for a POI
 2) Add new POI
 3) TOP 5 most popular POIs
 4) Add visits from GPX file
 5) Exit

If the user gives a wrong string, the program should give an error message and ask for the command again.

For answers 2,3 and 4, the program should just tell that this feature is not implemented yet, and ask for another command. 

5: simply exit the program

1: ask for a search string, then list out all the pois from in poi.json, that contain this string as a substring 
in their name (should NOT be case sensitive). When listing these POIs, list their name & position.


Hint: don't reimplement features, use a POI_Manager from 03 for Menu 1.

"""

import json
import unittest
import os

script_dir = os.path.dirname(__file__)

class POI_Manager:
  
    def __init__(self, poi_dateiname):
        self.file_path = os.path.join(script_dir, poi_dateiname)
    
    def get_poi_count(self) -> int:
        with open(self.file_path,'r',encoding="utf-8")as datei:
            data= json.load(datei)
        return len(data)
    
    def get_pois(self) -> set[str]:
        with open(self.file_path, 'r',encoding='utf-8')as datei:
             data = json.load(datei)
        namen_set = {item['name'] for item in data}
        return namen_set
    
    def get_pos(self, name:str)-> tuple[float, float] |None:
        with open(self.file_path,'r', encoding='utf-8' )as datei:
            data=json.load(datei)
        for item in data:
            if item['name']==name:
                return(item['pos']['lat'], item['pos']['lon'])
        return None
        
    def search_pois(self, search_string: str):
        with open(self.file_path, 'r', encoding='utf-8') as datei:
            data = json.load(datei)
        
        search_string = search_string.lower()
        results = []
        for item in data:
            if search_string in item['name'].lower():
                results.append(item)
        return results

while True:
    print("""
What do you want to do?
 1) Search for a POI
 2) Add new POI
 3) TOP 5 most popular POIs
 4) Add visits from GPX file
 5) Exit""")
    
    entscheidung= input("Welche Entscheidung?")

    if entscheidung == "1":
        poim = POI_Manager("poi_test.json")
        ort = input("Welcher POI?")
        ort_low = ort.lower
        print(poim.get_pos(ort)); print(ort)
    elif entscheidung == "2":
        print("this feature is not implemented yet")
    elif entscheidung == "3":
        print("this feature is not implemented yet")
    elif entscheidung == "4":
        print("this feature is not implemented yet")
    elif entscheidung == "5":
        quit()
    else:
        print("please choose a number between 1-5")


    
if __name__ == '__main__':
    pass

