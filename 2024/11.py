import functools
import math
import os
from typing import Iterator


def next_blink(stone: int) -> list[int]:
    result = []
    if stone == 0:
        result.append(1)
    else:
        digits = int(math.log10(stone)) + 1
        if digits % 2 == 0:
            p10 = int(10 ** (digits / 2))
            result.append(int(stone / p10))
            result.append(int(stone % p10))
        else:
            result.append(stone * 2024)
    return result


def part1(lines: Iterator[str]) -> None:
    line = next(lines).rstrip(os.linesep)
    stones = list(map(int, line.split()))
    all_stones = set(stones)
    for _ in range(25):
        new_stones = []
        for stone in stones:
            new_stones.extend(next_blink(stone))
        all_stones.update(new_stones)
        stones = new_stones
    print(f"Answer for 11.1 is {len(stones)}")
    print(len(all_stones))


@functools.cache
def down_the_tree(stone: int, levels_to_go: int) -> int:
    """
    Goes down the tree and returns the number of spawned stones.
    """
    spawns = next_blink(stone)
    if levels_to_go == 1:
        return len(spawns)
    result = down_the_tree(spawns[0], levels_to_go - 1)
    if len(spawns) > 1:
        result += down_the_tree(spawns[1], levels_to_go - 1)
    return result


def part2(lines: Iterator[str]) -> None:
    line = next(lines).rstrip(os.linesep)
    # line = "0"
    stones = list(map(int, line.split()))
    result = 0
    for stone in stones:
        result += down_the_tree(stone, 75)

    print(f"Answer for 11.2 is {result}")
