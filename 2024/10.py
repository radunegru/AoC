from dataclasses import dataclass
import os
from typing import Iterator


def char_int(c: str) -> int:
    try:
        return int(c)
    except ValueError:
        return -1


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def compute_trail(value: int, position: Point, topo: list[list[int]]) -> Iterator[Point]:
    # print(f"compute_trail({value=}, {position=})")
    max_value = len(topo)
    def get_next_point(point: Point) -> Iterator[Point]:
        def is_point(point: Point) -> bool:
            return (0 <= point.x < max_value) and (0 <= point.y < max_value)
        result = Point(point.x + 1, point.y    ) # right
        if is_point(result): yield result
        result = Point(point.x    , point.y + 1) # down
        if is_point(result): yield result
        result = Point(point.x - 1, point.y    ) # left
        if is_point(result): yield result
        result = Point(point.x    , point.y - 1) # up
        if is_point(result): yield result
    for next_point in get_next_point(position):
        next_value = topo[next_point.y][next_point.x]
        # message = f"({position.x}, {position.y}){value} --> ({next_point.x},{next_point.y}){next_value}"
        if next_value == value + 1:
            if next_value == 9:
                # print(f"{message} ... good")
                yield next_point
            else:
                # print(f"{message} ... continue")
                yield from compute_trail(next_value, next_point, topo)
        # else:
        #     print(f"{message} ... fail")


def compute_trails(trailhead: Point, topo: list[list[int]]) -> int:
    targets: set[Point] = set()
    for target in compute_trail(0, trailhead, topo):
        targets.add(target)
    # print(targets)
    return len(targets)


def part1(lines: Iterator[str]) -> None:
    # lines = iter([
    #     "0123",
    #     "1234",
    #     "8765",
    #     "9876",
    # ])
    # lines = iter([
    #     "...0...",
    #     "...1...",
    #     "...2...",
    #     "6543456",
    #     "7.....7",
    #     "8.....8",
    #     "9.....9",
    # ])
    # lines = iter([
    #     "..90..9",
    #     "...1.98",
    #     "...2..7",
    #     "6543456",
    #     "765.987",
    #     "876....",
    #     "987....",
    # ])
    # lines = iter([
    #     "10..9..",
    #     "2...8..",
    #     "3...7..",
    #     "4567654",
    #     "...8..3",
    #     "...9..2",
    #     ".....01",
    # ])
    topo: list[list[int]] = []
    for line in lines:
        line = line.rstrip(os.linesep)
        topo.append([height for height in map(char_int, line)])
    # find trailheads
    trailheads: list[Point] = []
    for y, row in enumerate(topo):
        x = -1
        while True:
            try:
                x = row.index(0, x + 1)
                trailheads.append(Point(x, y))
            except ValueError:
                break
    result = 0
    for trailhead in trailheads:
        result += compute_trails(trailhead, topo)

    print(f"Answer for 10.1 is {result}")


def part2(lines: Iterator[str]) -> None:
    topo: list[list[int]] = []
    for line in lines:
        line = line.rstrip(os.linesep)
        topo.append([height for height in map(char_int, line)])
    # find trailheads
    trailheads: list[Point] = []
    for y, row in enumerate(topo):
        x = -1
        while True:
            try:
                x = row.index(0, x + 1)
                trailheads.append(Point(x, y))
            except ValueError:
                break
    trails = 0
    for trailhead in trailheads:
        for _ in compute_trail(0, trailhead, topo):
            trails += 1
    print(f"Answer for 10.2 is {trails}")
