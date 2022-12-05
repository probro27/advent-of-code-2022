## Initial Structure - test.txt

#             [J] [Z] [G]            
#             [Z] [T] [S] [P] [R]    
# [R]         [Q] [V] [B] [G] [J]    
# [W] [W]     [N] [L] [V] [W] [C]    
# [F] [Q]     [T] [G] [C] [T] [T] [W]
# [H] [D] [W] [W] [H] [T] [R] [M] [B]
# [T] [G] [T] [R] [B] [P] [B] [G] [G]
# [S] [S] [B] [D] [F] [L] [Z] [N] [L]
#  1   2   3   4   5   6   7   8   9 

init_list = [['S', 'T', 'H', 'F', 'W', 'R'], ['S', 'G', 'D', 'Q', 'W'], ['B', 'T', 'W'], ['D', 'R', 'W', 'T', 'N', 'Q', 'Z', 'J'], ['F', 'B', 'H', 'G', 'L', 'V', 'T', 'Z'], ['L', 'P', 'T', 'C', 'V', 'B', 'S', 'G'], ['Z', 'B', 'R', 'T', 'W', 'G', 'P'], ['N', 'G', 'M', 'T', 'C', 'J', 'R'], ['L', 'G', 'B', 'W']]

## Sample structure - sample.txt

#     [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 

sample_list = [['Z', 'N'], ['M', 'C', 'D'], ['P']]

from typing import List
import sys

def parseInputRound1():
    # test
    init_list_copy = init_list
    # sample
    # init_list_copy = sample_list
    for line in sys.stdin:
        split_sentence = line.split(' ')
        number_of_boxes, initial_stack_n, final_stack_n = int(split_sentence[1]), int(split_sentence[3]), int(split_sentence[5])
        initial_stack = init_list_copy[initial_stack_n - 1]
        final_stack = init_list_copy[final_stack_n - 1]
        boxes_to_move = initial_stack[len(initial_stack) - number_of_boxes:]
        reverse_boxes_to_move = boxes_to_move[::-1]
        for element in reverse_boxes_to_move:
            final_stack.append(element)
        del initial_stack[len(initial_stack) - number_of_boxes: ]
        init_list_copy[initial_stack_n - 1] = initial_stack
        init_list_copy[final_stack_n - 1] = final_stack
    final_str = ''
    for element_list in init_list_copy:
        final_str += element_list[-1]
    return final_str

def parseInputRound2():
    init_list_copy = init_list
    # sample
    # init_list_copy = sample_list
    for line in sys.stdin:
        split_sentence = line.split(' ')
        number_of_boxes, initial_stack_n, final_stack_n = int(split_sentence[1]), int(split_sentence[3]), int(split_sentence[5])
        initial_stack = init_list_copy[initial_stack_n - 1]
        final_stack = init_list_copy[final_stack_n - 1]
        boxes_to_move = initial_stack[len(initial_stack) - number_of_boxes:]
        # reverse_boxes_to_move = boxes_to_move[::-1]
        for element in boxes_to_move:
            final_stack.append(element)
        del initial_stack[len(initial_stack) - number_of_boxes: ]
        init_list_copy[initial_stack_n - 1] = initial_stack
        init_list_copy[final_stack_n - 1] = final_stack
    final_str = ''
    for element_list in init_list_copy:
        final_str += element_list[-1]
    return final_str 

if __name__ == '__main__':
    # print(parseInputRound1())
    print(parseInputRound2())
        
