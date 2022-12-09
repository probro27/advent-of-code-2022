import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, MutableSet

class Direction(Enum):
    Left = auto()
    Right = auto()
    Up = auto()
    Down = auto()

@dataclass
class Move():
    direction: Direction
    steps: int
    
@dataclass
class Coordinate():
    x: int
    y: int
    def __hash__(self) -> int:
        return hash((self.x, self.y))

@dataclass
class Coordinate_update():
    x_update: int
    y_update: int
    
tail_movement_set: MutableSet[tuple] = set()
current_head_coordinate: Coordinate = Coordinate(0, 0)
current_tail_coordinate: Coordinate = Coordinate(0, 0)
    
def parseInput() -> List[Move]:
    head_move_list: List[Move] = []
    for line in sys.stdin:
        direction, steps = line.split(' ')
        direction_state: Direction = None
        if direction == 'L':
            direction_state = Direction.Left
        elif direction == 'R':
            direction_state = Direction.Right
        elif direction == 'U':
            direction_state = Direction.Up
        elif direction == 'D':
            direction_state = Direction.Down
        else:
            print(f'Why is it reaching here: {direction}')
        move = Move(direction=direction_state, steps=int(steps))
        head_move_list.append(move)
    return head_move_list

def are_head_tail_touching() -> bool:
    current_head_x, current_head_y = current_head_coordinate.x, current_head_coordinate.y
    current_tail_x, current_tail_y = current_tail_coordinate.x, current_tail_coordinate.y
    if current_head_x == current_tail_x:
        if current_head_y == current_tail_y + 1 or current_head_y == current_tail_y - 1:
            return True
        else:
            return False
    if current_tail_y == current_head_y:
        if current_head_x == current_tail_x + 1 or current_head_x == current_tail_x - 1:
            return True
        else:
            return False
    if (current_tail_x == current_head_x + 1 and (current_tail_y == current_head_y + 1 or current_tail_y == current_head_y - 1)) or (current_tail_x == current_head_x - 1 and (current_tail_y == current_head_y + 1 or current_tail_y == current_head_y - 1)):
        return True
    else:
        return False 
     
def how_to_update_y() -> Coordinate_update:
    current_head_x, current_head_y = current_head_coordinate.x, current_head_coordinate.y
    current_tail_x, current_tail_y = current_tail_coordinate.x, current_tail_coordinate.y
    coordinate_update = Coordinate_update(0, 0)
    # print(f'Adding coordinates: head: {current_head_coordinate}, tail: {current_tail_coordinate}')
    if current_head_x == current_tail_x:
        if current_head_y > current_tail_y + 1:
            coordinate_update.y_update = 1
        elif current_head_y < current_tail_y - 1:
            coordinate_update.y_update = -1
    elif current_head_y == current_tail_y:
        # print(f'Reached here')
        if current_head_x > current_tail_x + 1:
            # print(f'{current_head_x} > {current_tail_x + 1}')
            coordinate_update.x_update = 1
        elif current_head_x < current_tail_x - 1:
            coordinate_update.x_update = -1
    else:
        if not are_head_tail_touching():
            if current_head_y > current_tail_y:
                coordinate_update.y_update = 1
            elif current_head_y < current_tail_y:
                coordinate_update.y_update = -1
            if current_head_x > current_tail_x:
                coordinate_update.x_update = 1
            elif current_head_x < current_tail_x:
                coordinate_update.x_update = -1
    # print(f'Current head: {current_head_coordinate}, update: {coordinate_update}') 
    return coordinate_update

def move_one_direction(move: Move):
    direction, steps = move.direction, move.steps
    for step in range(steps):
        if direction == Direction.Left:
            current_head_coordinate.x -= 1
        elif direction == Direction.Right:
            current_head_coordinate.x += 1
        elif direction == Direction.Up:
            current_head_coordinate.y += 1
        elif direction == Direction.Down:
            current_head_coordinate.y -= 1
        coordinate_update = how_to_update_y()
        current_tail_coordinate.x += coordinate_update.x_update
        current_tail_coordinate.y += coordinate_update.y_update
        print(f'direction: {direction}, step: {step}, current_head: {current_head_coordinate.x, current_head_coordinate.y}, current_tail: {current_tail_coordinate.x, current_tail_coordinate.y}')
        tail_movement_set.add((current_tail_coordinate.x, current_tail_coordinate.y))
        
def move_all(head_move_list: List[Move]):
    for move in head_move_list:
        move_one_direction(move)

def count_distinct_tail_positions() -> int:
    return len(tail_movement_set)

if __name__ == '__main__':
    head_move_list = parseInput()
    move_all(head_move_list)
    print(tail_movement_set)
    print(count_distinct_tail_positions())
    # current_head_coordinate.x, current_head_coordinate.y = 2, 0
    # print(how_to_update_y())
