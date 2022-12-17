import sys
from typing import List, Dict, MutableSet, Tuple
from enum import Enum, auto
from dataclasses import dataclass
from pprint import pprint
from math import inf

class State(Enum):
    sensor = auto()
    beacon = auto()
    can_be_beacon = auto()
    cannot_be_beacon = auto()

@dataclass
class Coordinate:
    x: int
    y: int
    
@dataclass
class Point:
    coordinate: Coordinate
    state: State
    def __hash__(self) -> int:
        return hash((self.coordinate.x, self.coordinate.y))

print_dict: Dict[State, str] = {
    State.sensor: 'S',
    State.beacon: 'B',
    State.can_be_beacon: '.',
    State.cannot_be_beacon: '#'
}

class Beacon_zone:
    beacon_sensor_map: List[List[Point]]
    beacon_sensor_dict: Dict[Point, Point]
    line_number_considered: int
    
    def __init__(self):
        self.beacon_sensor_map = []
        self.beacon_sensor_dict = {}
        self.max_x = -1
        self.min_x = 100
        self.max_y = -1
        self.min_y = 100
        if (sys.argv[1] == '-s'):
            self.line_number_considered = 10
        elif sys.argv[1] == '-t':
            self.line_number_considered = 2000000
    
    def __parse_expression(self, exp: str) -> int:
        exp = exp.replace(',', '')
        exp_split = exp.split('=')
        return int(exp_split[1])
    
    def __assign_max_min_values(self, sensor_x: int, sensor_y: int, beacon_x: int, beacon_y: int):
        self.max_x = max(self.max_x, sensor_x, beacon_x)
        self.min_x = min(self.min_x, sensor_x, beacon_x)
        self.max_y = max(self.max_y, sensor_y, beacon_y)
        self.min_y = min(self.min_y, sensor_y, beacon_y)
    
    def __reverse_transform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        final_coordinate: Coordinate = Coordinate(coordinate.x + self.min_x, coordinate.y + self.min_y)
        return final_coordinate
    
    def __transform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        final_coordiante: Coordinate = Coordinate(coordinate.x - self.min_x, coordinate.y - self.min_y)
        return final_coordiante
    
    def parse_input(self):
        for line in sys.stdin:
            line = line.strip()
            sensor_line, beacon_line = [x.split(' ') for x in line.split(': ')]
            sensor_x, sensor_y = self.__parse_expression(sensor_line[2]), self.__parse_expression(sensor_line[3])
            beacon_x, beacon_y = self.__parse_expression(beacon_line[4]), self.__parse_expression(beacon_line[5]) 
            sensor_point = Point(Coordinate(sensor_x, sensor_y), State.sensor)
            beacon_point = Point(Coordinate(beacon_x, beacon_y), State.beacon)
            self.beacon_sensor_dict[sensor_point] = beacon_point
            self.__assign_max_min_values(sensor_x, sensor_y, beacon_x, beacon_y)
    
    def create_map(self):
        length = self.max_y - self.min_y + 1
        breadth = self.max_x - self.min_x + 1
        for x in range(length):
            individual_row: List[Point] = []
            for y in range(breadth):
                coordinate = self.__reverse_transform_coordinate(Coordinate(y, x))
                beacon = self.beacon_sensor_dict.get(Point(coordinate, State.sensor), None)
                if beacon is None:
                    individual_row.append(Point(coordinate, State.can_be_beacon))
                else:
                    individual_row.append(Point(coordinate, State.sensor))
            self.beacon_sensor_map.append(individual_row)
        for sensor in self.beacon_sensor_dict.keys():
            beacon = self.beacon_sensor_dict[sensor]
            beacon_coordiante = self.__transform_coordinate(beacon.coordinate)
            self.beacon_sensor_map[beacon_coordiante.y][beacon_coordiante.x].state = State.beacon
    
    def calculate_manhattan_distance(self, coordinate1: Coordinate, coordinate2: Coordinate) -> int:
        return abs(coordinate1.x - coordinate2.x) + abs(coordinate1.y - coordinate2.y)
        
    def find_beacons_on_row(self) -> int:
        row_being_considered = self.line_number_considered
        sensors = self.beacon_sensor_dict.keys()
        cannot_be_beacons = 0
        for sensor in sensors:
            closest_beacon = self.beacon_sensor_dict[sensor]
            closest_beacon_distance = self.calculate_manhattan_distance(sensor.coordinate, closest_beacon.coordinate)
            sensor_coordinate_transformed = self.__transform_coordinate(sensor.coordinate)
            starting_index_x = sensor_coordinate_transformed.x
            while starting_index_x >= 0:
                coordinate_to_check = Coordinate(self.__reverse_transform_coordinate(Coordinate(starting_index_x, 0)).x, row_being_considered)
                distance = self.calculate_manhattan_distance(sensor.coordinate, coordinate_to_check)
                if distance > closest_beacon_distance:
                    break
                if self.beacon_sensor_map[self.__transform_coordinate(Coordinate(0, row_being_considered)).y][starting_index_x].state != State.cannot_be_beacon and self.beacon_sensor_map[self.__transform_coordinate(Coordinate(0, row_being_considered)).y][starting_index_x].state != State.beacon:
                    self.beacon_sensor_map[self.__transform_coordinate(Coordinate(0, row_being_considered)).y][starting_index_x].state = State.cannot_be_beacon
                    cannot_be_beacons += 1
                print(sensor.coordinate, 2 * sensor_coordinate_transformed.x - starting_index_x, sensor_coordinate_transformed.x, starting_index_x)
                if 2 * sensor_coordinate_transformed.x - starting_index_x < self.max_x - self.min_x + 1 and starting_index_x != sensor_coordinate_transformed.x:
                    if self.beacon_sensor_map[self.__transform_coordinate(Coordinate(0, row_being_considered)).y][2* sensor_coordinate_transformed.x - starting_index_x].state != State.cannot_be_beacon and self.beacon_sensor_map[self.__transform_coordinate(Coordinate(0, row_being_considered)).y][2* sensor_coordinate_transformed.x - starting_index_x].state != State.beacon: 
                        self.beacon_sensor_map[self.__transform_coordinate(Coordinate(0, row_being_considered)).y][2* sensor_coordinate_transformed.x - starting_index_x].state = State.cannot_be_beacon
                        cannot_be_beacons += 1 
                starting_index_x -= 1
                
        return cannot_be_beacons
    
    def find_beacons_on_row_fast(self) -> int:
        cannot_be_beacons_list: Dict[Tuple[int, int], State] = {}
        row_being_considered = self.line_number_considered
        sensors = self.beacon_sensor_dict.keys()
        cannot_be_beacons = 0
        for sensor in sensors:
            closest_beacon = self.beacon_sensor_dict[sensor]
            closest_beacon_distance = self.calculate_manhattan_distance(sensor.coordinate, closest_beacon.coordinate)
            starting_index_x = sensor.coordinate.x
            while starting_index_x >= self.min_x:
                coordinate_to_check = Coordinate(starting_index_x, row_being_considered)
                distance = self.calculate_manhattan_distance(sensor.coordinate, coordinate_to_check)
                if distance > closest_beacon_distance:
                    break
                if cannot_be_beacons_list.get((coordinate_to_check.x,row_being_considered), None) is None and (coordinate_to_check.x, coordinate_to_check.y) != (closest_beacon.coordinate.x, closest_beacon.coordinate.y):
                    cannot_be_beacons += 1 
                    cannot_be_beacons_list[(coordinate_to_check.x,row_being_considered)] = State.cannot_be_beacon
                if cannot_be_beacons_list.get((2 * sensor.coordinate.x - coordinate_to_check.x, row_being_considered), None) is None and ((2 * sensor.coordinate.x - coordinate_to_check.x, row_being_considered)) != (closest_beacon.coordinate.x, closest_beacon.coordinate.y):
                    cannot_be_beacons += 1
                    cannot_be_beacons_list[(2 * sensor.coordinate.x - coordinate_to_check.x, row_being_considered)] = State.cannot_be_beacon
                starting_index_x -= 1
        return cannot_be_beacons
            
    def print_zone(self):
        for row in self.beacon_sensor_map:
            for element in row:
                print(print_dict[element.state], end=' ')
            print()
    
if __name__ == '__main__':
    beacon_zone = Beacon_zone()
    beacon_zone.parse_input()
    # Visualize the map
    # beacon_zone.create_map()
    # beacon_zone.print_zone()
    print(beacon_zone.line_number_considered)
    print(beacon_zone.find_beacons_on_row_fast())
    # Visualize the map after blocking
    # beacon_zone.print_zone()
    # print(beacon_zone.calculate_manhattan_distance(Coordinate(8, 7), Coordinate(1, 10)))
    # print(beacon_zone.calculate_manhattan_distance(Coordinate(8, 7), Coordinate(2, 10)))
    
    
    
