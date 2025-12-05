import os
from typing import Iterator


def look_and_say(sequence: str) -> str:
    pairs = []
    last_char = None
    count = 0
    for c in sequence:
        if (last_char is not None) and (c != last_char):
            pairs.append([count, last_char])
            count = 0
        last_char = c
        count += 1
    pairs.append([count, last_char])
    return "".join(f"{count}{c}" for count, c in pairs)


def part1(lines: Iterator[str]) -> None:
    for line in lines:
        line = line.rstrip(os.linesep)
        sequence = line
        for _ in range(40):
            sequence = look_and_say(sequence)
        print(f"Answer for 10.1 is {len(sequence)}")


def part2(lines: Iterator[str]) -> None:
    for line in lines:
        line = line.rstrip(os.linesep)
        sequence = line
        for _ in range(50):
            sequence = look_and_say(sequence)
        print(f"Answer for 10.2 is {len(sequence)}")
