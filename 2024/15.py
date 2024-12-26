from collections import defaultdict
import curses
import os
from typing import Iterator


class Warehouse1:
    def __init__(self):
        self.warehouse: list[list[str]] = []
        self.robot: tuple[int, int] = (-1, -1)
        self.count: defaultdict[str, int] = defaultdict(int)

    def read_warehouse(self, lines: Iterator[str]) -> None:
        self.warehouse = []
        it_lines = enumerate(lines)
        for r, line in it_lines:
            if line == "\n": break
            row: list[str] = []
            for c, cell in enumerate(line):
                row.append(cell)
                if cell == "@":
                    self.robot = (r, c)
                self.count[cell] += 1
            self.warehouse.append(row)

    def print_warehouse(self, window: curses.window) -> None:
        for r, row in enumerate(self.warehouse):
            window.move(r, 0)
            for cell in row:
                if cell == "@":
                    window.addch(cell, curses.color_pair(1))
                else:
                    window.addch(cell)
        window.move(len(self.warehouse), 0)
        window.addstr(f"Robot @ ({self.robot[0], self.robot[1]})\n")

    def move_robot(self, dx: int, dy: int) -> None:
        def can_move(dx: int, dy: int) -> bool:
            x = self.robot[1] + dx; y = self.robot[0] + dy
            while self.warehouse[y][x] != "#":
                if self.warehouse[y][x] == ".":
                    return True
                x += dx; y += dy
            return False
        if not can_move(dx, dy): return
        to_replace: str = "."
        x = self.robot[1]; y = self.robot[0]
        while True:
            current_cell = self.warehouse[y][x]
            self.warehouse[y][x] = to_replace
            to_replace = current_cell
            if to_replace == ".":
                break
            x += dx; y += dy
        self.robot = (self.robot[0] + dy, self.robot[1] + dx)

    def gps_sum(self) -> int:
        result: int = 0
        for r, row in enumerate(self.warehouse):
            for c, cell in enumerate(row):
                if cell == "O":
                    result += 100 * r + c
        return result


def do_part1(scr_main: curses.window, lines: Iterator[str]) -> int:
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    warehouse = Warehouse1()
    warehouse.read_warehouse(lines)
    warehouse.print_warehouse(scr_main)
    scr_main.refresh()

    while True:
        try:
            line = next(lines)
            dx = dy = 0
            for move in line.rstrip(os.linesep):
                match move:
                    case "^":
                        dx = 0; dy = -1
                    case "v":
                        dx = 0; dy = +1
                    case "<":
                        dx = -1; dy = 0
                    case ">":
                        dx = +1; dy = 0
                warehouse.move_robot(dx, dy)
                warehouse.print_warehouse(scr_main)
                scr_main.refresh()
                # curses.napms(10)

        except StopIteration:
            break

    result = warehouse.gps_sum()
    scr_main.addstr(f"Answer for 15.1 is {result}")
    scr_main.getch()
    return result


def part1(lines: Iterator[str]) -> None:
    # lines = iter([
    #     "########\n",
    #     "#..O.O.#\n",
    #     "##@.O..#\n",
    #     "#...O..#\n",
    #     "#.#.O..#\n",
    #     "#...O..#\n",
    #     "#......#\n",
    #     "########\n",
    #     "\n", 
    #     "<^^>>>vv<v>>v<<\n"
    # ])
    result = curses.wrapper(do_part1, lines)
    print(f"Answer for 15.1 is {result}")


class Warehouse2:
    def __init__(self):
        self.warehouse: list[list[str]] = []
        self.robot: tuple[int, int] = (-1, -1)
        self.count: defaultdict[str, int] = defaultdict(int)

    def read_warehouse(self, lines: Iterator[str]) -> None:
        self.warehouse = []
        it_lines = enumerate(lines)
        for r, line in it_lines:
            if line == "\n": break
            row: list[str] = []
            for c, cell in enumerate(line):
                match cell:
                    case "#":
                        row.append("#")
                        row.append("#")
                    case "O":
                        row.append("[")
                        row.append("]")
                    case ".":
                        row.append(".")
                        row.append(".")
                    case "@":
                        row.append("@")
                        row.append(".")
                        self.robot = (r, c * 2)
                self.count[cell] += 1
            self.warehouse.append(row)

    def print_warehouse(self, window: curses.window) -> None:
        for r, row in enumerate(self.warehouse):
            window.move(r, 0)
            for cell in row:
                if cell == "@":
                    window.addch(cell, curses.color_pair(1))
                else:
                    window.addch(cell)
        window.move(len(self.warehouse), 0)
        window.addstr(f"Robot @ ({self.robot[0], self.robot[1]})\n")

    def move_horz(self, dx: int) -> None:
        movements: dict[tuple[int, int], str] = { self.robot: "." }
        y = self.robot[0]; current_x = self.robot[1]; current_cell = "@"
        while current_cell != ".":
            x = current_x + dx
            if self.warehouse[y][x] == "#":
                return  # blocked by wall, do not move
            movements[(y, x)] = current_cell
            current_x = x
            current_cell = self.warehouse[y][x]
        for pos, block in movements.items():
            self.warehouse[pos[0]][pos[1]] = block
        self.robot = (self.robot[0], self.robot[1] + dx)

    def move_vert(self, dy: int) -> None:
        movable: set[tuple[int, int]] = {self.robot}
        movements: dict[tuple[int, int], str] = {}
        while len(movable) > 0:
            to_ckeck: tuple[int, int] = movable.pop()
            if to_ckeck not in movements:
                movements[to_ckeck] = "."
            current_y = to_ckeck[0]; x = to_ckeck[1]; current_cell = self.warehouse[current_y][x]
            while current_cell != ".":
                y = current_y + dy
                match self.warehouse[y][x]:
                    case "#":
                        return  # blocked by wall, do not move
                    case "[":
                        movable.add((y, x + 1))
                    case "]":
                        movable.add((y, x - 1))
                    case ".":
                        pass
                    case _:
                        raise Exception(f"Unexpected {current_cell} @ ({y}{x}) KABOOM!!!\n")
                movements[(y, x)] = current_cell
                current_y = y
                current_cell = self.warehouse[y][x]
        for pos, block in movements.items():
            self.warehouse[pos[0]][pos[1]] = block
        self.robot = (self.robot[0] + dy, self.robot[1])


    def gps_sum(self) -> int:
        result: int = 0
        for r, row in enumerate(self.warehouse):
            for c, cell in enumerate(row):
                if cell == "[":
                    result += 100 * r + c
        return result


def do_part2(scr_main: curses.window, lines: Iterator[str]) -> int:
    curses.init_pair(255, curses.COLOR_WHITE, 0xE8)
    scr_main.bkgd(" ", curses.color_pair(255))
    curses.init_pair(1, curses.COLOR_RED, 0xE8)
    warehouse = Warehouse2()
    warehouse.read_warehouse(lines)
    warehouse.print_warehouse(scr_main)
    scr_main.refresh()

    while True:
        try:
            line = next(lines)
            for move in line.rstrip(os.linesep):
                scr_main.addstr(move)
                scr_main.refresh()
                match move:
                    case "^":
                        warehouse.move_vert(-1)
                    case "v":
                        warehouse.move_vert(+1)
                    case "<":
                        warehouse.move_horz(-1)
                    case ">":
                        warehouse.move_horz(+1)
                # scr_main.move(0, 0)
                warehouse.print_warehouse(scr_main)
                scr_main.refresh()
        except StopIteration:
            break

    result = warehouse.gps_sum()
    scr_main.addstr(f"Answer for 15.2 is {result}")
    scr_main.refresh()
    scr_main.getch()
    return result


def part2(lines: Iterator[str]) -> None:
    # lines = iter([
    #     "#######\n",
    #     "#...#.#\n",
    #     "#.....#\n",
    #     "#..OO@#\n",
    #     "#..O..#\n",
    #     "#.....#\n",
    #     "#######\n",
    #     "\n",
    #     "<vv<<^^<<^^\n"
    # ])
    result = curses.wrapper(do_part2, lines)
    print(f"Answer for 15.2 is {result}")
