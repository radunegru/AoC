import os
import re
from typing import Iterator


class Grid1:
    SIZE: int = 1000
    def __init__(self):
        self._grid = []
        for _ in range(0, self.SIZE):
            self._grid.append([ False ] * self.SIZE)

    def turn_on(self, rectangle: tuple[int, int, int, int]) -> None:
        x1, y1, x2, y2 = rectangle
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self._grid[x][y] = True

    def turn_off(self, rectangle: tuple[int, int, int, int]) -> None:
        x1, y1, x2, y2 = rectangle
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self._grid[x][y] = False

    def toggle(self, rectangle: tuple[int, int, int, int]) -> None:
        x1, y1, x2, y2 = rectangle
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self._grid[x][y] = not self._grid[x][y]

    def count_on(self) -> int:
        result = 0
        for x in range(0, self.SIZE):
            for y in range(0, self.SIZE):
                if self._grid[x][y]:
                    result += 1
        return result

    def print(self) -> None:
        for x in range(0, self.SIZE):
            for y in range(0, self.SIZE):
                print(self._grid[x][y], end="")
                print(" ", end="")
            print()


def part1(lines: Iterator[str]) -> None:
    grid = Grid1()
    re_instruction = r"(?P<action>turn on|turn off|toggle) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)"
    # lines = [
    #     "turn on 0,0 through 999,999",
    #     "toggle 0,0 through 999,0",
    #     "turn off 499,499 through 500,500"
    #     # "turn off 999,999 through 999,999"
    # ]
    for line in lines:
        line = line.rstrip(os.linesep)
        m = re.search(re_instruction, line)
        rectangle = ( \
            int(m.group("x1")), int(m.group("y1")), \
            int(m.group("x2")), int(m.group("y2")) \
        )
        match m.group("action"):
            case "turn on":
                grid.turn_on(rectangle)
            case "turn off":
                grid.turn_off(rectangle)
            case "toggle":
                grid.toggle(rectangle)
            case _:
                raise Exception(line)
    print(f"Answer for 6.1 is {grid.count_on()}")


class Grid2:
    SIZE = 1000
    def __init__(self):
        self._grid = []
        for _ in range(0, self.SIZE):
            self._grid.append([ 0 ] * self.SIZE)

    def turn_on(self, rectangle: tuple[int, int, int, int]) -> None:
        x1, y1, x2, y2 = rectangle
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self._grid[x][y] += 1

    def turn_off(self, rectangle: tuple[int, int, int, int]) -> None:
        x1, y1, x2, y2 = rectangle
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self._grid[x][y] = max(0, self._grid[x][y] - 1)

    def toggle(self, rectangle: tuple[int, int, int, int]) -> None:
        x1, y1, x2, y2 = rectangle
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self._grid[x][y] += 2

    def count_brightness(self) -> int:
        result = 0
        for x in range(0, self.SIZE):
            for y in range(0, self.SIZE):
                result += self._grid[x][y]
        return result

    def print(self) -> None:
        for x in range(0, self.SIZE):
            for y in range(0, self.SIZE):
                print(self._grid[x][y], end="")
                print(" ", end="")
            print()


def part2(lines: Iterator[str]) -> None:
    grid = Grid2()
    re_instruction = r"(?P<action>turn on|turn off|toggle) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)"
    # lines = [
    #     "turn on 0,0 through 0,0",
    #     "toggle 0,0 through 999,999",
    #     "turn off 0,0 through 0,0",
    # ]
    for line in lines:
        line = line.rstrip(os.linesep)
        m = re.search(re_instruction, line)
        rectangle = ( \
            int(m.group("x1")), int(m.group("y1")), \
            int(m.group("x2")), int(m.group("y2")) \
        )
        match m.group("action"):
            case "turn on":
                grid.turn_on(rectangle)
            case "turn off":
                grid.turn_off(rectangle)
            case "toggle":
                grid.toggle(rectangle)
            case _:
                raise Exception(line)
    # grid.print()
    print(f"Answer for 6.1 is {grid.count_brightness()}")
