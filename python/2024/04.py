import os
from typing import Iterator


def get_char(big:list[str], x: int, y: int) -> str:
    if 0 <= x < len(big):
        line = big[x]
        if 0 <= y < len(line):
            return line[y]
    return "a"


def part1(lines: Iterator[str]) -> None:
    big: list[str] = [line.rstrip(os.linesep) for line in lines]
    count = 0
    for x in range(len(big)):
        line = big[x]
        for y in range(len(line)):
            for incx in range(-1, 2):
                for incy in range(-1, 2):
                    if (incx == 0) and (incy == 0): continue
                    word = "".join([ get_char(big, x + i * incx, y + i * incy) for i in range(0, 4) ])
                    if word == "XMAS":
                        count += 1

    print(f"Answer for 4.1 is {count}")


def part2(lines: Iterator[str]) -> None:
    big: list[str] = [line.rstrip(os.linesep) for line in lines]
    count = 0
    for x in range(len(big)):
        line = big[x]
        for y in range(len(line)):
            if line[y] == "A":
                word1 = "".join([get_char(big, x - 1, y - 1), "A", get_char(big, x + 1, y + 1)])
                word2 = "".join([get_char(big, x - 1, y + 1), "A", get_char(big, x + 1, y - 1)])
                if (word1 in ["MAS", "SAM"]) and (word2 in ["MAS", "SAM"]):
                    count += 1

    print(f"Answer for 4.2 is {count}")
