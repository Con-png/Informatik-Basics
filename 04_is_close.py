"""

Write two functions:
 - one to return the estimated distance of 2 points
 - one to tell, if two points are close or not (=within the distance of a provided treshold value)

For an estimation, you can assume, that lon/lat are 2D coordinates on a flat surface, and around this region:

1 latitude degree = 111 km
1 longitude degree = 75 km

Moreover the treshold value should have a default of 50 meters.


"""


def distance(pos1:tuple[float,float], pos2:tuple[float,float]) -> float:
    lat1, lon1 = pos1
    lat2, lon2 = pos2

    delta_lat = lat2-lat1
    delta_lon = lon2-lon1

    delta_lat *= 111
    delta_lon *= 75

    dist = (delta_lat**2+delta_lon**2)**(1/2)
    return dist

def is_close(pos1:tuple[float,float], pos2:tuple[float,float], threshold_m:float) -> bool:
    dist = distance(pos1,pos2)
    threshold_m = 0.05
    if dist > threshold_m:
        return False
    else:
        return True


# Tests 

import unittest
class Test_Distance(unittest.TestCase):

    def test_distance(self):
        pass

    def test_is_close(self):
        pass

if __name__ == '__main__':
    unittest.main()

