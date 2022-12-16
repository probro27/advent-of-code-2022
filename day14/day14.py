import sys
from typing import List, Dict
from enum import Enum, auto
from dataclasses import dataclass
from copy import deepcopy
from pprint import pprint
from more_itertools import pairwise

class State(Enum):
    air = auto()
    rock = auto()
    sand = auto()

@dataclass
class Coordinate:
    x: int
    y: int

    def __lt__(self, __o: object) -> bool:
        return self.x < __o.x and self.y < __o.y # type: ignore
 
@dataclass
class AreaBlock:
    coordinate: Coordinate
    state: State

state_transform = {
    State.rock: '#',
    State.air: '.',
    State.sand: 'o'
}

class Area:
    cave_map: List[List[AreaBlock]]
    cave_map_dict: Dict[int, Dict[int, AreaBlock]]
    smallest_coordinate: Coordinate
    largest_coordinate: Coordinate
    x_offset: int
    y_offset: int
    map_length: int
    map_width: int
    current_sand_position: Coordinate
    sand_grains_fell: int
    sand_falls_void: bool

    def __init__(self):
        self.cave_map = []
        self.cave_map_dict = dict()
        self.smallest_coordinate = None # type: ignore 
        self.largest_coordinate = None # type: ignore   
        self.x_offset = -1
        self.y_offset = -1
        self.map_length = 0
        self.map_width = 0
        self.current_sand_position = Coordinate(500, 0)
        self.sand_grains_fell = 0
        self.sand_falls_void = False
        
    def coordinate_transform(self, coordinate: Coordinate) -> Coordinate:
        final_coordinate = Coordinate(0, 0)
        final_coordinate.x = coordinate.x - self.x_offset
        final_coordinate.y = coordinate.y
        return final_coordinate
    
    def reverse_coordinate_transform(self, coordinate: Coordinate) -> Coordinate:
        final_coordinate = Coordinate(0, 0)
        final_coordinate.x = self.x_offset + coordinate.x
        final_coordinate.y = coordinate.y
        return final_coordinate

    def parse_input(self, part: int = 1):
        for line in sys.stdin:
            split_line = line.split(' -> ')
            split_line_coordinate = [AreaBlock(Coordinate(int(x.split(',')[0]), int(x.split(',')[1])), State.rock) for x in split_line]
            for area1, area2 in pairwise(split_line_coordinate):
                row = area1.coordinate.x
                col = area1.coordinate.y
                row2 = area2.coordinate.x
                col2 = area2.coordinate.y
                if row > row2:
                    temp = row2
                    row2 = row
                    row = temp
                if col > col2:
                    temp = col2
                    col2 = col
                    col = temp
                for index in range(row, row2 + 1):
                    for column in range(col, col2 + 1): 
                        area_to_add = AreaBlock(Coordinate(index, column), State.rock)
                        if index not in self.cave_map_dict.keys():
                            self.cave_map_dict[index] = { column: area_to_add }
                        else:
                            self.cave_map_dict[index][column] = area_to_add
                        if self.smallest_coordinate is None:
                            self.smallest_coordinate = Coordinate(index, column)
                        else:
                            if self.smallest_coordinate.x > index:
                                self.smallest_coordinate.x = index
                            if self.smallest_coordinate.y > column:
                                self.smallest_coordinate.y = column
                        if self.largest_coordinate is None:
                            self.largest_coordinate = Coordinate(index, column)
                        else:
                            if self.largest_coordinate.x < index:
                                self.largest_coordinate.x = index
                            if self.largest_coordinate.y < column:
                                self.largest_coordinate.y = column
        self.map_length = self.largest_coordinate.x - self.smallest_coordinate.x
        self.map_width = self.largest_coordinate.y # - self.smallest_coordinate.y (we want 0 for sand)
        if part == 2:
            self.smallest_coordinate.x -= 500
            self.largest_coordinate.x += 500
        else:
            self.smallest_coordinate.x -= 1
            self.largest_coordinate.x += 1
        self.smallest_coordinate.y = 0
        self.x_offset = self.smallest_coordinate.x
        self.y_offset = 0 # not self.smallest_coordinate.y (sand enters at 0)

    def create_map(self, part: int = 1):
        for area_block in range(self.smallest_coordinate.x, self.largest_coordinate.x + 1):
            individual_line: List[AreaBlock] = []
            rock_rows = self.cave_map_dict.get(area_block)
            if rock_rows is None:
                for y in range(self.smallest_coordinate.y, self.largest_coordinate.y + 1):
                    individual_line.append(AreaBlock(Coordinate(area_block, y), State.air))
            else:
                for y in range(self.smallest_coordinate.y, self.largest_coordinate.y + 1):
                    rock = rock_rows.get(y)
                    if rock is None:
                        individual_line.append(AreaBlock(Coordinate(area_block, y), State.air))
                    else:
                        individual_line.append(rock)
            if part == 2:
                individual_line.append(AreaBlock(Coordinate(area_block, self.largest_coordinate.y + 1), State.air))
                individual_line.append(AreaBlock(Coordinate(area_block, self.largest_coordinate.y + 2), State.rock))
            self.cave_map.append(individual_line)
        self.current_sand_position = Coordinate(500, 0)
        update_coordinate = self.coordinate_transform(self.current_sand_position)
        self.cave_map[update_coordinate.x][update_coordinate.y].state = State.sand
    
    def create_map_2(self):
        self.create_map(2)
    
    def find_sand_drop_position(self, sand_position: Coordinate):
        current_sand_position_transformed = self.coordinate_transform(sand_position)
        cave_row = self.cave_map[current_sand_position_transformed.x]
        first_rock_in_path = next((x for x in cave_row if (lambda y: (y.state == State.rock or y.state == State.sand) and y.coordinate.y > current_sand_position_transformed.y)(x)), None)
        if first_rock_in_path is None:
            self.cave_map[current_sand_position_transformed.x][self.largest_coordinate.y].state = State.sand
            self.sand_falls_void = True
            return
        else:
            current_sand_position = Coordinate(first_rock_in_path.coordinate.x, first_rock_in_path.coordinate.y - 1)
            current_sand_position_transform = self.coordinate_transform(current_sand_position)
            if self.cave_map[(current_sand_position_transform.x - 1)][current_sand_position_transform.y + 1].state == State.air:
                new_sand_position = self.reverse_coordinate_transform(Coordinate(current_sand_position_transform.x - 1, current_sand_position_transform.y + 1))
                self.find_sand_drop_position(new_sand_position)
                return
            elif self.cave_map[(current_sand_position_transform.x + 1)][current_sand_position_transform.y + 1].state == State.air: 
                new_sand_position = self.reverse_coordinate_transform(Coordinate(current_sand_position_transform.x + 1, current_sand_position_transform.y + 1))
                self.find_sand_drop_position(new_sand_position)
                return
            else:
                new_sand_position = self.reverse_coordinate_transform(current_sand_position_transform)
                self.current_sand_position = new_sand_position
                return
            
    def find_sand_drop_position_2(self, sand_position: Coordinate):
        current_sand_position_transformed = self.coordinate_transform(sand_position)
        cave_row = self.cave_map[current_sand_position_transformed.x]
        first_rock_in_path = next((x for x in cave_row if (lambda y: (y.state == State.rock or y.state == State.sand) and y.coordinate.y > current_sand_position_transformed.y)(x)), None)
        if first_rock_in_path is not None:
            current_sand_position = Coordinate(first_rock_in_path.coordinate.x, first_rock_in_path.coordinate.y - 1)
            current_sand_position_transform = self.coordinate_transform(current_sand_position)
            if self.cave_map[(current_sand_position_transform.x - 1)][current_sand_position_transform.y + 1].state == State.air:
                new_sand_position = self.reverse_coordinate_transform(Coordinate(current_sand_position_transform.x - 1, current_sand_position_transform.y + 1))
                self.find_sand_drop_position_2(new_sand_position)
                return
            elif self.cave_map[(current_sand_position_transform.x + 1)][current_sand_position_transform.y + 1].state == State.air: 
                new_sand_position = self.reverse_coordinate_transform(Coordinate(current_sand_position_transform.x + 1, current_sand_position_transform.y + 1))
                self.find_sand_drop_position_2(new_sand_position)
                return
            else:
                new_sand_position = self.reverse_coordinate_transform(current_sand_position_transform)
                self.current_sand_position = new_sand_position
                return  
              
    def simulate_sand_drop(self):
        while True:
            previous_sand_position = deepcopy(self.current_sand_position)
            self.find_sand_drop_position(self.current_sand_position)
            if self.sand_falls_void == True:
                return
            self.sand_grains_fell += 1
            sand_position_list = self.coordinate_transform(self.current_sand_position)
            self.cave_map[sand_position_list.x][sand_position_list.y].state = State.sand
            previous_sand_position_list = self.coordinate_transform(previous_sand_position)
            self.current_sand_position = Coordinate(500, 0)
            current_sand_position_list = self.coordinate_transform(self.current_sand_position)
            self.cave_map[previous_sand_position_list.x][previous_sand_position_list.y].state = State.air
            self.cave_map[current_sand_position_list.x][current_sand_position_list.y].state = State.sand
            
    def simulate_sand_drop_2(self):
        while True:
            previous_sand_position = deepcopy(self.current_sand_position)
            self.find_sand_drop_position_2(self.current_sand_position)
            if self.current_sand_position.x == 500 and self.current_sand_position.y == 0:
                self.sand_grains_fell += 1
                return
            self.sand_grains_fell += 1
            sand_position_list = self.coordinate_transform(self.current_sand_position)
            self.cave_map[sand_position_list.x][sand_position_list.y].state = State.sand
            previous_sand_position_list = self.coordinate_transform(previous_sand_position)
            self.current_sand_position = Coordinate(500, 0)
            current_sand_position_list = self.coordinate_transform(self.current_sand_position)
            self.cave_map[previous_sand_position_list.x][previous_sand_position_list.y].state = State.air
            self.cave_map[current_sand_position_list.x][current_sand_position_list.y].state = State.sand
    
    def print_cave_map(self):
        transpose_list = [[state_transform[row[i].state] for row in self.cave_map] for i in range(len(self.cave_map[0]))]
        pprint(transpose_list)
        
    
    
if __name__ == '__main__':
    area = Area()
    # Part 1
    area.parse_input()
    area.create_map()
    area.simulate_sand_drop()
    print(area.sand_grains_fell)
    area.print_cave_map()
    # # Part 2
    area.parse_input(part=2)
    area.create_map_2()
    area.simulate_sand_drop_2()
    print(area.sand_grains_fell)
    area.print_cave_map()
