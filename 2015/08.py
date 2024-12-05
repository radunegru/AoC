import os
from typing import Iterator


def part1(lines: Iterator[str]) -> None:
    result = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        s = eval(line)
        result += len(line) - len(s)

    print(f"Answer for 8.1 is {result}")


def part2(lines: Iterator[str]) -> None:
    result = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        s = line.replace("\\", "\\\\")
        s = s.replace("\"", "\\\"")
        s = f"\"{s}\""
        result += len(s) - len(line)

    print(f"Answer for 8.2 is {result}")
