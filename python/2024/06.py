from dataclasses import dataclass, field
import os
from typing import Iterator


STANCES = [
    ( 0, -1), #up
    (+1,  0), #right
    ( 0, +1), #down
    (-1,  0), #left
]
DIRECTIONS = "^>v<"


def print_map1(the_map: list[list[str]]) -> None:
    for row in the_map:
        print("".join(row))


def part1(lines: Iterator[str]) -> None:
    the_map: list[list[str]] = []
    x_guard, y_guard, direction = -1, -1, 0
    c_line = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        the_map.append([c for c in line])
        guard = line.find("^")
        if guard != -1:
            x_guard = guard
            y_guard = c_line
        c_line += 1
    c_steps = 1
    the_map[y_guard][x_guard] = "X"
    b_guard_in_map = True
    while b_guard_in_map and (c_steps < len(the_map) * len(the_map)):
        for i in range(4):
            stance = STANCES[(direction + i) % 4]
            new_x = x_guard + stance[0]
            new_y = y_guard + stance[1]
            # print(f"({x_guard},{y_guard}) -> ({new_x},{new_y})")
            if the_map[new_y][new_x] == "#":
                continue
            if the_map[new_y][new_x] != "X":
                c_steps += 1
            the_map[new_y][new_x] = "X"
            if (new_y == 0) or (new_y == len(the_map) - 1) or (new_x == 0) or (new_x == len(the_map[new_y]) - 1):
                b_guard_in_map = False
            x_guard = new_x
            y_guard = new_y
            direction = direction + i
            break

    print(f"Answer for 6.1 is {c_steps}")


@dataclass
class MapPoint():
    """
    . - neutral
    # - given obstacle
    X - visited
    O - tentative obstacle
    ^ - initial guard
    """
    style: str = "."
    """
    Guard directions while passing through the point:
    - 0 - up
    - 1 - right
    - 2 - down
    - 3 - left
    """
    directions: set[int] = field(default_factory=set)
    generation: int = 0


def print_map2(the_map: list[list[MapPoint]]) -> None:
    print("\033[2J\033[H", end="")
    for row in the_map:
        print("".join([mp.style for mp in row]))


def part2(lines: Iterator[str]) -> None:
    the_map: list[list[MapPoint]] = []
    original_x_guard, original_y_guard, direction = -1, -1, 0
    c_line = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        the_map.append([MapPoint(style=c) for c in line])
        guard = line.find("^")
        if guard != -1:
            original_x_guard = guard
            original_y_guard = c_line
        c_line += 1
    generation = 0
    good_obstacles: list[tuple[int, int]] = []
    for y in range(len(the_map)):
        for x in range(len(the_map[y])):
            print(f"\033[2K\r{y},{x}", end="")
            # x, y = 5, 6
            # print(f"{the_map[4][6]=}")
            # input(f"Initalizing, press Enter to continue")
            generation += 1
            old_style = the_map[y][x].style
            if old_style == "#": continue

            c_steps = 1
            the_map[y][x].style = "O"
            the_map[original_y_guard][original_x_guard].directions = { 0 }
            the_map[original_y_guard][original_x_guard].generation = generation
            x_guard, y_guard, direction = original_x_guard, original_y_guard, 0
            b_guard_in_map = True
            while b_guard_in_map and (c_steps < len(the_map) * len(the_map)):
                # breakpoint()
                for i in range(4):
                    current_direction = (direction + i) % 4
                    stance = STANCES[current_direction]
                    new_x = x_guard + stance[0]
                    new_y = y_guard + stance[1]
                    new_point = the_map[new_y][new_x]
                    if new_point.style in [ "#", "O" ]:
                        continue
                    if (new_y == 0) or (new_y == len(the_map) - 1) or (new_x == 0) or (new_x == len(the_map[new_y]) - 1):
                        b_guard_in_map = False
                    if (new_point.generation == generation) and (current_direction in new_point.directions):
                        good_obstacles.append((x, y))
                        b_guard_in_map = False
                        # print_map2(the_map)
                        # print(f"Found looping obstacle at ({x=}, {y=})")
                        # print(f"{direction=}, {current_direction=}, {i=}, {x_guard=}, {y_guard=}, {new_x=}, {new_y=}")
                        # print(f"{the_map[new_y][new_x]}")
                        # input("Press Enter to continue")
                        break
                    new_point.style = "X"
                    if new_point.generation == generation:
                        new_point.directions.add(current_direction)
                    else:
                        # if (new_x == 6) and (new_y == 4):
                        #     print(f"Change generation of ({new_x}, {new_y}) from {new_point.generation} to {generation}")
                        #     input("...")
                        new_point.directions = { current_direction }
                        new_point.generation = generation
                    x_guard = new_x
                    y_guard = new_y
                    # print_map2(the_map)
                    # print(f"direction={DIRECTIONS[direction]}, current={DIRECTIONS[current_direction]}, {i=}, {generation=}")
                    # print(f"{the_map[4][6]=}")
                    # input(f"Moving, press Enter to continue {b_guard_in_map}")
                    direction = (direction + i) % 4
                    break
            if b_guard_in_map:
                print("Fail............")
            # revert the map
            the_map[y][x].style = old_style
            for reset_y in range(len(the_map)):
                for reset_x in range(len(the_map[reset_y])):
                    reset_point = the_map[reset_y][reset_x]
                    if reset_point.style == "X":
                        reset_point.style = "."
                        # reset_point.generation = 0
            the_map[original_y_guard][original_x_guard].style = "^"

    print(f"Answer for 6.2 is {len(good_obstacles)}")
    # for obstacle in good_obstacles:
    #     print(f"    {obstacle}")
