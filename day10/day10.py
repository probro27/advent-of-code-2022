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

signal_check_cycle_list :List[int] = [20, 60, 100, 140, 180, 220]
signal_strength_list: List[int] = []
    
@dataclass
class Signal:
    opeation: Operation
    register_value: int | None

@dataclass
class ClockCircuit:
    register: int
    cycle: int

clock_circuit = ClockCircuit(1, 0)

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

def check_cycle():
    if clock_circuit.cycle in signal_check_cycle_list:
        signal_strength_list.append(clock_circuit.register)

def perform_noop():
    clock_circuit.cycle += 1
    check_cycle()
    
def perform_addx(value: int):
    clock_circuit.cycle += 1
    check_cycle()
    clock_circuit.cycle += 1
    check_cycle()
    clock_circuit.register += value

def perform_all_operations(signal_list: List[Signal]):
    for signal in signal_list:
        if signal.opeation == Operation.noop:
            perform_noop()
        else:
            perform_addx(signal.register_value)

def sum_signal_cycle() -> int:
    product_list = [signal_check_cycle_list[i] * signal_strength_list[i] for i in range(6)]
    return sum(product_list)

if __name__ == '__main__':
    signal_list = parseInput()
    perform_all_operations(signal_list)
    print(signal_strength_list)
    print(sum_signal_cycle())
