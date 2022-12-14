import sys
from dataclasses import dataclass
from typing import List, Tuple
import operator
from tqdm import tqdm
from math import lcm
from functools import reduce

@dataclass
class Item:
    worry_level: int

@dataclass
class Monkey:
    starting_items: List[Item]
    operation: Tuple[str, int] | None
    divisible_test: int
    true_monkey: int
    false_monkey: int
    items_inspected: int
    
    def __copy__(self):
        monkey = Monkey(self.starting_items, self.operation, self.divisible_test, self.true_monkey, self.false_monkey, self.items_inspected)
        return monkey
    
resolve_operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

monkey_list: List[Monkey] = []
number_of_rounds: int = 10000

def parseInput():
    is_monkey_data_being_processed = False
    current_monkey: Monkey | None = None
    for line in sys.stdin:
        line = line.strip()
        if is_monkey_data_being_processed and current_monkey:
            split_line = line.split(' ')
            if split_line[0] == 'Starting':
                items_list = split_line[2: ]
                items_str = ' '.join(map(str, items_list))
                items_split = items_str.split(', ')
                items_split_int = [int(x) for x in items_split]
                items = [Item(x) for x in items_split_int]
                current_monkey.starting_items = items
            elif split_line[0] == 'Operation:':
                operation = split_line[4]
                try:
                    number = int(split_line[5])
                except:
                    number = 0
                current_monkey.operation = (operation, number)
            elif split_line[0] == 'Test:':
                current_monkey.divisible_test = int(split_line[3])
            elif split_line[0] == 'If':
                if split_line[1] == 'true:':
                    current_monkey.true_monkey = int(split_line[5])
                elif split_line[1] == 'false:':
                    current_monkey.false_monkey = int(split_line[5])
                    is_monkey_data_being_processed = False
                    monkey_list.append(current_monkey.__copy__())
                    current_monkey = None
        else:
            current_monkey = Monkey([], None, 0, -1, -1, 0)
            is_monkey_data_being_processed = True

def item_inspection(current_monkey_index: int, current_item_index: int, common_mod: int):
    current_monkey = monkey_list[current_monkey_index]
    if current_monkey.operation:
        current_item = current_monkey.starting_items[current_item_index]
        if current_monkey.operation[1] == 0:
            current_item.worry_level = int(resolve_operators[current_monkey.operation[0]](current_item.worry_level, current_item.worry_level)) % common_mod
        else:
            current_item.worry_level = int(resolve_operators[current_monkey.operation[0]](current_item.worry_level, current_monkey.operation[1])) % common_mod
        current_monkey.items_inspected += 1
    
def find_monkey_to_hand_item(current_monkey_index: int, current_item_index: int) -> int:
    current_monkey = monkey_list[current_monkey_index]
    current_item = current_monkey.starting_items[current_item_index]
    monkey_to_return_to = -1
    if current_item.worry_level % current_monkey.divisible_test == 0:
        monkey_to_return_to = current_monkey.true_monkey
    else:
        monkey_to_return_to = current_monkey.false_monkey
    return monkey_to_return_to    

def monkey_simulation(current_monkey_index: int, common_mod: int):
    current_monkey = monkey_list[current_monkey_index]
    items_list = current_monkey.starting_items
    for index, item in enumerate(items_list):
        item_inspection(current_monkey_index, index, common_mod)
        monkey_to_pass_item = find_monkey_to_hand_item(current_monkey_index, index)
        monkey_to_pass = monkey_list[monkey_to_pass_item]
        monkey_to_pass.starting_items.append(item)
    current_monkey.starting_items = []
          
def round_simulation(common_mod):
    for index, _ in enumerate(monkey_list):
        monkey_simulation(index, common_mod)

def game_simulation(common_mod):
    for round in tqdm(range(number_of_rounds), desc='Rounds'):
        round_simulation(common_mod)
        # print(f'Round {round} completed');
        
def find_monkey_business() -> int:
    sorted_monkey_list = sorted(monkey_list, key=lambda monkey: monkey.items_inspected, reverse=True)
    return sorted_monkey_list[0].items_inspected * sorted_monkey_list[1].items_inspected

if __name__ == '__main__':
    parseInput()
    divisibile_list = [x.divisible_test for x in monkey_list]
    common_mod = reduce(lcm, divisibile_list)
    game_simulation(common_mod)
    print(find_monkey_business())
