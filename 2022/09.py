from math import sqrt
from typing import Iterator


UNIT_VECTORS = { "U": 1j, "D": -1j, "L": -1, "R": 1 }
SQRT2 = sqrt(2)


def moves_generator(lines: Iterator[str]) -> Iterator[list[str]]:
    for line in lines:
        yield line.strip().split()


def move_tail(moves: Iterator[list[str]], length: int) -> set[complex]:
    rope = [ 0j ] * length
    tail_positions = set()
    for direction, steps in moves:
        for _ in range(int(steps)):
            rope[0] += UNIT_VECTORS[direction]
            for n in range(1, len(rope)):
                diff = rope[n - 1] - rope[n]
                if abs(diff) > SQRT2:
                    if diff.real != 0:
                        rope[n] += diff.real / abs(diff.real)
                    if diff.imag != 0:
                        rope[n] += complex(0, diff.imag) / abs(diff.imag)
            tail_positions.add(rope[-1])
    return tail_positions


def part1(lines: Iterator[str]) -> None:
    tail_positions = move_tail(moves_generator(lines), 2)
    print(f"Answer for 9.1 is {len(tail_positions)}")


def part2(lines: Iterator[str]) -> None:
    tail_positions = move_tail(moves_generator(lines), 10)
    print(f"Answer for 9.2 is {len(tail_positions)}")
