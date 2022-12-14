from dataclasses import dataclass
from typing import List
import sys
from copy import deepcopy
import ast
from functools import cmp_to_key

@dataclass
class Pair:
    left: List[any] | int
    right: List[any] | int
    
    def __copy__(self) -> object:
        new_pair = Pair(deepcopy(self.left), deepcopy(self.right))
        return new_pair
class distress_signal:
    signal_pair_list: List[Pair]
    
    def __init__(self, _signal_pair_list: List[Pair]):
        self.signal_pair_list = _signal_pair_list
    
    def compare_signal_pair(self, pair_left: any, pair_right: any) -> (bool | None):
        if type(pair_left) == list and type(pair_right) == list:
            if len(pair_left) == 0 and len(pair_right) != 0:
                return True
            if len(pair_right) == 0 and len(pair_left) != 0:
                return False
            if len(pair_left) == 0 and len(pair_right) == 0:
                return None
            
            for index in range(min(len(pair_left), len(pair_right))):
                val =  self.compare_signal_pair(pair_left[index], pair_right[index])
                if val is not None:
                    return val

            if len(pair_left) < len(pair_right):
                return True
            elif len(pair_left) > len(pair_right):
                return False
            else:
                return None
        elif type(pair_left) == int and type(pair_right) == int:
            if pair_left < pair_right:
                return True
            elif pair_left > pair_right:
                return False
            else:
                return None
        elif type(pair_left) == list and type(pair_right) == int:
            return self.compare_signal_pair(pair_left, [pair_right])
        elif type(pair_left) == int and type(pair_right) == list:
            return self.compare_signal_pair([pair_left], pair_right)
        
    def find_sum_comparisons(self) -> int:
        final_sum = 0
        for index, pair in enumerate(self.signal_pair_list):
            compare = self.compare_signal_pair(pair.left, pair.right)
            if compare is None or compare == True:
                final_sum += index + 1
        return final_sum
    
    def sort_comparer(self, item1: List[any], item2: List[any]):
        val = self.compare_signal_pair(item1, item2)
        if val == True:
            return -1
        if val == False:
            return 1
        if val is None:
            return 0
    
    def common_list(self) -> List[any]:
        final_list= []
        for pair in self.signal_pair_list:
            final_list.append(pair.left)
            final_list.append(pair.right)
        return final_list
    
    def find_sorted_list(self):
        common_list = self.common_list()
        common_list.append([[2]])
        common_list.append([[6]])
        common_list.sort(key=cmp_to_key(self.sort_comparer))
        return common_list
    
    def find_decoded_signal(self, common_list: list) -> int:
        index1 = common_list.index([[2]])
        index2 = common_list.index([[6]])
        return (index1 + 1) * (index2 + 1)

def find_elements_to_delete(final_list_last_element: List[any]) -> int:
    value = 0
    for element in final_list_last_element:
        if type(element) == list:
            value += 2 + find_elements_to_delete(element)
        else:
            value += 1
    return value

def eval_parse_input():
    distress_signal_send: distress_signal = None
    signal_list: List[Pair] = []
    is_pair_open = False
    current_pair: Pair = Pair([], [])
    for line in sys.stdin:
        if line == '\n':
            signal_list.append(current_pair.__copy__())
            current_pair = Pair([], [])
            continue
        line = line.strip()
       
        if is_pair_open:
            current_pair.right = ast.literal_eval(line)
            is_pair_open = False
        else:
            current_pair.left = ast.literal_eval(line)
            is_pair_open = True
    signal_list.append(current_pair.__copy__())
    distress_signal_send = distress_signal(signal_list)
    return distress_signal_send 
        
            
if __name__ == '__main__':
    distress_signal = eval_parse_input()
    print(f'Part 1: {distress_signal.find_sum_comparisons()}')
    common_list = distress_signal.find_sorted_list()
    print(f'Part 2: {distress_signal.find_decoded_signal(common_list)}')
