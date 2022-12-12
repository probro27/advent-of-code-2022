import sys
from dataclasses import dataclass
from typing import List, Tuple, MutableSet, Deque
from collections import deque

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
    deque: Deque[Tuple[int, Coordinate]]
    ended: bool
    
    
    def __init__(self, starting_position: Coordinate, ending_position: Coordinate):
        self.coordinate = starting_position
        self.number_of_steps_travelled = 0
        self.starting_position = starting_position
        self.ending_position = ending_position
        self.previous_coordinates = set()
        self.previous_coordinates.add(starting_position)
        self.deque = deque()
        self.deque.append((0, starting_position))
        self.ended = False
    
    def decide_next_move(self, steps: int, coordinate_to_check: Coordinate):
        r, c = coordinate_to_check.x, coordinate_to_check.y
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr < 0 or nc < 0 or nr >= len(elevation_map) or nc >= len(elevation_map[0]):
                continue
            if Coordinate(nr, nc) in self.previous_coordinates:
                continue
            if elevation_map[nr][nc] - elevation_map[r][c] > 1:
                continue
            if nr == ending_position.x and nc == ending_position.y:
                self.number_of_steps_travelled = steps + 1
                self.ended = True
                return
            self.previous_coordinates.add(Coordinate(nr, nc))
            self.deque.append((steps + 1, Coordinate(nr, nc)))
        
    
    def simulate_movement(self):
        while self.deque and not self.ended:
            steps, coordinate_to_check = self.deque.popleft()
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
