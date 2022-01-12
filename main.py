import math
import mapbox
from mapbox import Directions

help(mapbox.Directions)


def map_test():
    service = Directions()
    origin = {
        'type': 'Feature',
        'properties': {'name': 'Portland, OR'},
        'geometry': {
            'type': 'Point',
            'coordinates': [-122.7282, 45.5801]}}
    destination = {
        'type': 'Feature',
        'properties': {'name': 'Bend, OR'},
        'geometry': {
            'type': 'Point',
            'coordinates': [-121.3153, 44.0582]}}
    destination1 = {
        'type': 'Feature',
        'properties': {'name': 'Bend, OR'},
        'geometry': {
            'type': 'Point',
            'coordinates': [-122, 45]}}
    response = service.directions([origin, destination1, destination], 'mapbox/walking', alternatives=True, continue_straight=True, geometries='geojson', language='en', overview='simplified', steps=False).geojson()
    return response


def check_intersection(directions, avoidCoordinates, radius):
    # Determines whether the avoid location is RADIUS units from the path
    # Directions class contains the current directions that are being tested
    # avoidCoordinates are the coordinates of the point we are avoiding
    waypoints = directions.getWaypoints()
    coordinates = directions.getCoordinates()
    for i in range(len(waypoints) - 1):
        tempWaypoints = list()
        for j in range(i):
            tempWaypoints.append(waypoints[j])
        tempWaypoints.append(avoidCoordinates)
        tempDirections = getDirections(tempWaypoints)
        tempCoordinates = tempDirections.getCoordinates()
        iter = 0
        while iter < len(coordinates) and iter < len(tempCoordinates):
            if coordinates[iter][0] == tempCoordinates[iter][0] and coordinates[iter][1] == tempCoordinates[iter][1]:
                # compares whether coordinates are the same at ITER coordinate might need to change and give linency with less than abs
                iter += 1
            else:
                # coordinates don't match iter is divergent point
                break
        divergentCoordinate = tempCoordinates[iter]
        divergentDistance = distanceCoordinates(divergentCoordinate, avoidCoordinates)
        distanceToDivergent = distanceCoordinates(tempCoordinates[iter - 1], divergentCoordinate)
        distanceToNextCoordinate = distanceCoordinates(coordinates[iter - 1], coordinates[iter])
        if divergentDistance > radius or distanceToDivergent > distanceToNextCoordinate:
            pass
        else:
            return False
    return True


def distanceCoordinates(coordinate0, coordinate1):
    coordinateDistance = math.sqrt(coordinate0 ** 2 + coordinate1 ** 2)
    return coordinateDistance * 111139


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(map_test())  # ['features'][0]['geometry']['coordinates']

# See PyCharm help at https://www.jetbrains.com/help/pycharm/