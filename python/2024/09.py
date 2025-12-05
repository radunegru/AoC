from collections import defaultdict
from dataclasses import dataclass
import os
from typing import Iterator


def part1(lines: Iterator[str]) -> None:
    for line in lines:
        line = line.rstrip(os.linesep)
        direct_file_index = -1
        free_space = 0
        for i, c in enumerate(line):
            if i % 2 == 0:
                direct_file_index += 1
            else:
                free_space += int(c)

        direct_file_index = -1
        direct_index = -1
        reverse_file_index = len(line) >> 1
        reverse_index = len(line) - 1
        c_reverse = int(line[reverse_index])
        freed_space = 0
        checksum = 0
        for i, c in enumerate(line):
            block_length = int(c)
            if i % 2 == 0:
                direct_file_index += 1
                for _ in range(block_length):
                    direct_index += 1
                    checksum += direct_file_index * direct_index
            else:
                for _ in range(block_length):
                    direct_index += 1
                    checksum += reverse_file_index * direct_index
                    freed_space += 1
                    c_reverse -= 1
                    if c_reverse == 0:
                        reverse_file_index -= 1
                        reverse_index -= 1
                        freed_space += int(line[reverse_index])
                        reverse_index -= 1
                        c_reverse = int(line[reverse_index])
            if freed_space == free_space:
                while c_reverse > 0:
                    direct_index += 1
                    checksum += reverse_file_index * direct_index
                    c_reverse -= 1
                break

        print(f"Answser for 9.1 is {checksum}")


@dataclass
class File:
    disk_index: int
    length: int # in blocks


def print_file_index(file_index: int):
    print(f"\033[s\033[{1+10};1H{file_index:4}\033[0K\033[u", end="")


def print_free_space(length: int, free_space_list: list[int]) -> None:
    print(f"\033[s\033[{length + 12};1H{length:2} -- {len(free_space_list):5} {free_space_list[0]:5}\033[0K\033[u", end="")


def print_all_free_space(free_space_dict: defaultdict[int, list[int]]) -> None:
    for i in range(10):
        print_free_space(i, free_space_dict[i])


def part2(lines : Iterator[str]) -> None:
    for line in lines:
        line = line.rstrip(os.linesep)

        # The list of files: the index is the file index
        files: list[File] = []
        # Dictionary of free space: length -> list of first disk index in block
        free_space_dict: defaultdict[int, list[int]]= defaultdict(list)
        disk_index = 0
        for i, c in enumerate(line):
            block_length = int(c)
            if i % 2 == 0:
                files.append(File(disk_index, block_length))
            else:
                free_space_dict[block_length].append(disk_index)
            disk_index += block_length

        # Start from last file index in reverse order
        for file_index in range(len(files) - 1, -1, -1):
            file = files[file_index]
            file_disk_index = file.disk_index

            free_block_length = 0
            free_block_index = file_disk_index
            for i in range(file.length, 10):
                if len(free_space_dict[i]) == 0:
                    continue
                candidate_free_block_index = free_space_dict[i][0]
                if candidate_free_block_index < free_block_index:
                    free_block_length = i
                    free_block_index = candidate_free_block_index
            if free_block_length == 0:
                # No free block of enough size available before the file
                continue
            # Move the file the the new position
            file.disk_index = free_space_dict[free_block_length].pop(0)
            # Free the space previously occupied by the file (not really necessary)
            free_space_dict[file.length].append(file_disk_index)
            free_space_dict[file.length].sort()
            delta = free_block_length - file.length
            if delta != 0:
                # Create a new free block
                free_space_dict[delta].append(free_block_index + file.length)
                free_space_dict[delta].sort()
        checksum = 0
        for file_index, file in enumerate(files):
            for l in range(file.length):
                checksum += file_index * (l + file.disk_index)

        print(f"Answer for 9.2 is {checksum}")
