from dataclasses import dataclass
from typing import List, Dict
import sys
import pprint

@dataclass
class File:
    file_name: str
    size: float

@dataclass
class Directory:
    files: List[File]
    sub_directories: Dict[str, any]
    dir_name: str
    size: float
    parent_directory: any

# Three cases - 
    # Command
        # cd (name) - going ahead
        # cd .. - going behind
        # ls - listing
    # dir
    # file

def find_all_directories_less_than_100000(root: Directory):
    all_dir_satisfying_property = []
    def recursive(dir):
        for directory in dir.sub_directories.keys():
            child_directory = dir.sub_directories[directory]
            recursive(child_directory)
        if dir.size <= 100000:
            all_dir_satisfying_property.append(dir)
    recursive(root)
    return all_dir_satisfying_property

def list_all_directories(root: Directory):
    all_dir = []
    def recursive(dir):
        for directory in dir.sub_directories.keys():
            child_directory = dir.sub_directories[directory]
            recursive(child_directory)
        all_dir.append(dir)
    recursive(root)
    return all_dir

def parseInput():
    root_directory = Directory([], {}, '/', 0, None)
    current_directory = root_directory
    for line in sys.stdin:
        line = line.strip()
        split_line = line.split(' ')
        if split_line[0] == '$':
            if split_line[1] == 'cd':
                if split_line[2] == '..':                    
                    for directory in current_directory.sub_directories.keys():
                        current_directory.size += current_directory.sub_directories[directory].size
                    current_directory = current_directory.parent_directory
                else:
                    new_directory_name = split_line[2]
                    # print(f"Cd into this {new_directory_name}")
                    # print(f"Current directories sub directories: {current_directory.sub_directories}")
                    current_directory = current_directory.sub_directories[new_directory_name]
            elif split_line[1] == 'ls':
                continue
        elif split_line[0].isnumeric():
            new_file = File(split_line[1], split_line[0])
            current_directory.files.append(new_file)
            current_directory.size += int(split_line[0])
        elif split_line[0] == 'dir':
            directory_name = split_line[1]
            current_directory.sub_directories[directory_name] = Directory([], {}, directory_name, 0, current_directory)
    for directory in root_directory.sub_directories.keys():
        root_directory.size += root_directory.sub_directories[directory].size
    
    return root_directory

def sum_all_files_all_directories(all_directories: List[Directory]):
    final_sum = 0
    for directory in all_directories:
        for file in directory.files:
            final_sum += int(file.size)
    return final_sum

def sum_all_directories(all_directories: List[Directory]):
    final_sum = 0
    for directory in all_directories:
        final_sum += directory.size
    return final_sum

if __name__ == '__main__':
    root_directory = parseInput()
    pprint.pprint(root_directory)
    # Part 1
    # all_directories = find_all_directories_less_than_100000(root_directory)
    # print(sum_all_directories(all_directories))
    all_directories = list_all_directories(root_directory)
    # sum_of_all_directories = sum_all_directories(all_directories)
    sum_of_all_directories = sum_all_files_all_directories(all_directories=all_directories)
    print(f"sum of all: {sum_of_all_directories}")
    difference_needed = sum_of_all_directories - 40000000
    print(f"difference needed: {difference_needed}")
    if difference_needed > 0:
        filter_less_than_diff = list(filter(lambda dir: dir.size >= difference_needed, all_directories))
        sorted_min_directories = sorted(filter_less_than_diff, key=lambda dir: (dir.size - difference_needed))
        # filter_greater_than_0 = list(filter(lambda dir: dir.size > 0, sorted_min_directories))
        # filter_greater_than_0.sort(key=lambda dir: dir.size)
        print(f"Delete: {sorted_min_directories[0].dir_name} with size: {sorted_min_directories[0].size}")
