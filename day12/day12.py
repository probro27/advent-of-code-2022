import sys
from dataclasses import dataclass
from typing import List, Tuple, MutableSet

@dataclass
class Coordinate:
    x: int
    y: int
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

class Person:
    coordinate: Coordinate
    number_of_steps_travelled: int
    starting_position: Coordinate
    ending_position: Coordinate
    previous_coordinates: MutableSet[Coordinate]
    bfs: List[Tuple[int, Coordinate]]
    ended: bool
    
    
    def __init__(self, starting_position: Coordinate, ending_position: Coordinate):
        self.coordinate = starting_position
        self.number_of_steps_travelled = 0
        self.starting_position = starting_position
        self.ending_position = ending_position
        self.previous_coordinates = set()
        self.previous_coordinates.add(starting_position)
        self.bfs: List[Tuple[int, Coordinate]] = []
        self.bfs.append((0, starting_position))
        self.ended = False
    
    def decide_next_move(self, steps: int, coordinate_to_check: Coordinate):
        row, col = coordinate_to_check.x, coordinate_to_check.y
        for check_row, check_col in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            if (check_row < 0 or check_col < 0 or check_row >= len(elevation_map) or 
                check_col >= len(elevation_map[0])) or Coordinate(check_row, check_col) in self.previous_coordinates or elevation_map[check_row][check_col] - elevation_map[row][col] > 1:
                continue
            if check_row == ending_position.x and check_col == ending_position.y:
                self.number_of_steps_travelled = steps + 1
                self.ended = True
                return
            self.previous_coordinates.add(Coordinate(check_row, check_col))
            self.bfs.append((steps + 1, Coordinate(check_row, check_col)))
        
    
    def simulate_movement(self):
        while self.bfs and not self.ended:
            steps, coordinate_to_check = self.bfs.pop(0)
            self.decide_next_move(steps, coordinate_to_check)
            
        
    def get_total_steps_travelled(self):
        return self.number_of_steps_travelled    

elevation_map: List[List[int]] = []

def parse_input() -> Tuple[List[Coordinate], Coordinate]:
    starting_position: List[Coordinate] = []
    ending_position: Coordinate = None  
    for index, line in enumerate(sys.stdin):
        line = line.strip()
        split_line = list(line)
        current_row = []
        for col, elevation in enumerate(split_line):
            if elevation == 'S':
                starting_position.append(Coordinate(index, col))
                current_row.append(ord('a') - 96)
            elif elevation == 'E':
                ending_position = Coordinate(index, col)
                current_row.append(ord('z') - 96)
            else:
                if elevation == 'a':
                    starting_position.append(Coordinate(index, col))
                current_row.append(ord(elevation) - 96)
        elevation_map.append(current_row)
    return (starting_position, ending_position)
        


if __name__ == '__main__':
    starting_positions, ending_position = parse_input()
    all_steps: List[Tuple[Coordinate, int]] = []
    for starting_position in starting_positions:
        person = Person(starting_position, ending_position)
        person.simulate_movement()
        if person.get_total_steps_travelled() != 0:
            all_steps.append((starting_position, person.get_total_steps_travelled()))
    all_steps.sort(key=lambda x: x[1])
    print(all_steps[0][1])
