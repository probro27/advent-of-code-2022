from dataclasses import dataclass
from typing import List
from multipledispatch import dispatch

# Attempt to use function overloading
# in progress
@dataclass
class Pair:
    left: List[any] | int
    right: List[any] | int

class distress_signal:
    signal_pair_list: List[Pair]
    
    def __init__(self, _signal_pair_list: List[Pair]):
        self.signal_pair_list = _signal_pair_list
    
    @dispatch(object, list, list)
    def compare_signal_pair(self, pair_left: List[any], pair_right: List[any]) -> (bool | None):
        if type(pair_left) == 'list' and type(pair_right) == 'list':
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
            else:
                return False
        
        
    @dispatch(object, int, int)
    def compare_signal_pair(self, pair_left: int, pair_right: int) -> (bool | None):
        if pair_right > pair_left:
            return True
        elif pair_right < pair_left:
            return False
        else:
            return None
    
    @dispatch(object, int, list)
    def compare_signal_pair(self, pair_left: int, pair_right: List[any]) -> (bool | None):
        pair_left_lst: List[int] = [pair_left]
        return self.compare_signal_pair(pair_left=pair_left_lst, pair_right=pair_right)
    
    @dispatch(object, list, int)
    def compare_signal_pair(self, pair_left: List[any], pair_right: int) -> (bool | None):
        pair_right_lst: List[int] = [pair_right]
        return self.compare_signal_pair(pair_left=pair_left, pair_right=pair_right_lst)
    
    
if __name__ == '__main__':
    distress_signal = distress_signal([Pair([1, 1, 3, 1, 1], [1, 1, 5, 1, 1])])
    print(distress_signal.compare_signal_pair(pair_left=distress_signal.signal_pair_list[0].left, pair_right=distress_signal.signal_pair_list[0].right))
