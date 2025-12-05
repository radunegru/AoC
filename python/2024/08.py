from dataclasses import dataclass
import os
from typing import Iterator


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def add_antinodes1(freq_antennas: list[Point], antinodes: set[Point], max_coord: int) -> None:
    l = len(freq_antennas)
    def add_antinodes_int(ref_antenna: Point, start: int, antinodes: set[Point]) -> None:
        for j in range(start, l):
            pair_antenna = freq_antennas[j]
            x1 = 2 * ref_antenna.x - pair_antenna.x
            y1 = 2 * ref_antenna.y - pair_antenna.y
            x2 = 2 * pair_antenna.x - ref_antenna.x
            y2 = 2 * pair_antenna.y - ref_antenna.y
            print(f"{ref_antenna} and {pair_antenna}: ", end="")
            if (0 <= x1 < max_coord) and (0 <= y1 < max_coord):
                antinodes.add(Point(x1, y1))
                print(f"({x1}, {y1})", end="")
            if (0 <= x2 < max_coord) and (0 <= y2 < max_coord):
                antinodes.add(Point(x2, y2))
                print(f" ({x2}, {y2})", end="")
            print()

    for i in range(l):
        ref_antenna = freq_antennas[i]
        add_antinodes_int(ref_antenna, i + 1, antinodes)


def add_antinodes2(freq_antennas: list[Point], antinodes: set[Point], max_coord: int) -> None:
    l = len(freq_antennas)
    def add_antinodes_int(ref_antenna: Point, start: int, antinodes: set[Point]) -> None:
        for j in range(start, l):
            pair_antenna = freq_antennas[j]
            dx = ref_antenna.x - pair_antenna.x
            dy = ref_antenna.y - pair_antenna.y
            c = 0
            print(f"{ref_antenna} and {pair_antenna}: ", end="")
            while True:
                x = ref_antenna.x + c * dx
                y = ref_antenna.y + c * dy
                if (0 <= x < max_coord) and (0 <= y < max_coord):
                    antinodes.add(Point(x, y))
                    print(f"({x}, {y})", end="")
                else:
                    break
                c += 1
            c = -1
            while True:
                x = ref_antenna.x + c * dx
                y = ref_antenna.y + c * dy
                if (0 <= x < max_coord) and (0 <= y < max_coord):
                    antinodes.add(Point(x, y))
                else:
                    break
                c -= 1
            print()

    for i in range(l):
        ref_antenna = freq_antennas[i]
        add_antinodes_int(ref_antenna, i + 1, antinodes)


def part(lines: Iterator[str], add_antinodes) -> int:
    all_antennas  = {}
    max_coord = -1
    for y, line in enumerate(lines):
        line = line.rstrip(os.linesep)
        max_coord = max(max_coord, len(line))
        for x, frequency in enumerate(line):
            if frequency != ".":
                freq_antennas = all_antennas.get(frequency, [])
                freq_antennas.append(Point(x=x, y=y))
                all_antennas[frequency] = freq_antennas

    antinodes = set()
    for frequency, freq_antennas in all_antennas.items():
        add_antinodes(freq_antennas, antinodes, max_coord)

    return len(antinodes)


def part1(lines: Iterator[str]) -> None:
    print(f"Answer to 8.1 is {part(lines, add_antinodes1)}")


def part2(lines: Iterator[str]) -> None:
    # lines = [
    #     "T.........",
	# "...T......",
	# ".T........",
	# "..........",
	# "..........",
	# "..........",
	# "..........",
	# "..........",
	# "..........",
	# ".........."
    # ]
    print(f"Answer to 8.2 is {part(lines, add_antinodes2)}")
