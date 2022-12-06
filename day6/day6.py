import sys

def parseInputRound1(n: int):
    total_processed_characters = 0
    start_limit = 0
    end_limit = n
    entire_string = ''
    for line in sys.stdin:
        entire_string += line
    
    while end_limit <= len(entire_string):
        four_letter_sequence = entire_string[start_limit:end_limit]
        hash_set = set()
        for letter in four_letter_sequence:
            hash_set.add(letter)
        if len(hash_set) == n:
            total_processed_characters = end_limit
            break
        start_limit += 1
        end_limit += 1
    
    return total_processed_characters

if __name__ == '__main__':
    # print(parseInputRound1(4))
    print(parseInputRound1(14))
