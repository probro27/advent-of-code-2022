import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class Operation(Enum):
    noop = auto()
    addx = auto()
    
cycle_map = {
    Operation.noop: 1,
    Operation.addx: 2
}

@dataclass
class Signal:
    opeation: Operation
    register_value: int | None

@dataclass
class ClockCircuit:
    register: int
    cycle: int

clock_circuit = ClockCircuit(1, 0)
final_pattern: List[List[str]] = []
current_sprite_position = [0, 1, 2]

def parseInput() -> List[Signal]:
    signal_list: List[Signal] = []
    for line in sys.stdin:
        line = line.strip()
        split_line = line.split()
        signal: Signal
        if split_line[0] == 'noop':
            signal = Signal(Operation.noop, None)
        else:
            signal = Signal(Operation.addx, int(split_line[1]))
        signal_list.append(signal)
    return signal_list

def check_cycle_divisible_forty():
    if (clock_circuit.cycle - 1) % 40 == 0:
        final_pattern.append([])

def add_light_or_dark():
    row = (clock_circuit.cycle - 1) // 40
    column = (clock_circuit.cycle - 1) % 40
    if column in current_sprite_position:
        final_pattern[row].append('#')
    else:
        final_pattern[row].append('.')

def perform_noop():
    clock_circuit.cycle += 1
    check_cycle_divisible_forty()
    add_light_or_dark()

def perform_addx(value: int):
    clock_circuit.cycle += 1
    check_cycle_divisible_forty()
    add_light_or_dark()
    clock_circuit.cycle += 1
    check_cycle_divisible_forty()
    add_light_or_dark()
    clock_circuit.register += value
    for index, element in enumerate(current_sprite_position):
        current_sprite_position[index] = element + value

def perform_all_operations(signal_list: List[Signal]):
    for signal in signal_list:
        if signal.opeation == Operation.noop:
            perform_noop()
        else:
            perform_addx(signal.register_value)

if __name__ == '__main__':
    signal_list = parseInput()
    perform_all_operations(signal_list=signal_list)
    for row in final_pattern:
        print(''.join(map(str, row)))
