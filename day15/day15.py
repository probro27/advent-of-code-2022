import sys
from typing import List, Dict
from enum import Enum, auto
from dataclasses import dataclass
from pprint import pprint

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

class Beacon_zone:
    beacon_sensor_map: List[List[Point]]
    beacon_sensor_dict: Dict[Point, Point]
    
    def __init__(self):
        self.beacon_sensor_map = []
        self.beacon_sensor_dict = {}
        self.max_x = -1
        self.min_x = -1
        self.max_y = -1
        self.min_y = -1
    
    def __parse_expression(self, exp: str) -> int:
        exp = exp.replace(',', '')
        exp_split = exp.split('=')
        return int(exp_split[1])
    
    def __assign_max_min_values(self, sensor_x: int, sensor_y: int, beacon_x: int, beacon_y: int):
        self.max_x = max(self.max_x, sensor_x, beacon_x)
        self.min_x = min(self.min_x, sensor_x, beacon_x)
        self.max_y = max(self.max_y, sensor_y, beacon_y)
        self.min_y = min(self.min_y, sensor_y, beacon_y)
    
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
        print(f'Length: {length}, Breadth: {breadth}')
        
        

if __name__ == '__main__':
    beacon_zone = Beacon_zone()
    beacon_zone.parse_input()
    beacon_zone.create_map()
