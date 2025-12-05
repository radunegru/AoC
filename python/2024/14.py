from collections import defaultdict
from dataclasses import dataclass
import re
import sys
from typing import Iterator


W = 101; H = 103


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int


def pretty_print_pos(pos: defaultdict[tuple[int, int], int], space_in_middle: bool=True) -> None:
    global W, H

    for y in range(H):
        for x in range(W):
            if space_in_middle and ((y == H // 2) or (x == W // 2)):
                print(" ", end="")
                continue
            if (x, y) in pos:
                print(pos[(x, y)], end="")
            else:
                print(".", end="")
        print()


def read_robots(lines: Iterator[str]) -> list[Robot]:
    global W, H

    if ("--test" in sys.argv) or ("-t" in sys.argv):
        W = 11; H = 7
    re_robot = r"^p=(?P<x>\d+),(?P<y>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)$"
    robots: list[Robot] = []
    for line in lines:
        m = re.match(re_robot, line)
        if m:
            robots.append(Robot(
                int(m.group("x")),
                int(m.group("y")),
                int(m.group("vx")),
                int(m.group("vy"))
            ))
    return robots


def part1(lines: Iterator[str]) -> None:
    global W, H

    robots = read_robots(lines)

    t = 100
    q1 = 0; q2 = 0; q3 = 0; q4 = 0
    pos100: defaultdict[tuple[int, int], int] = defaultdict(int)
    for robot in robots:
        x = (robot.x + t * robot.vx) % W
        y = (robot.y + t * robot.vy) % H
        pos100[(x, y)] += 1
        if x < W // 2:
            if y < H // 2:
                q1 += 1
            elif y > H // 2:
                q3 += 1
        elif x > W // 2:
            if y < H // 2:
                q2 += 1
            elif y > H // 2:
                q4 += 1
    pretty_print_pos(pos100)
    print(q1, q2, q3, q4)

    print(f"Answer for 14.1 is {q1 * q2 * q3 * q4}")


def part2(lines: Iterator[str]) -> None:
    robots = read_robots(lines)

    t = 0
    pos: defaultdict[tuple[int, int], int] = defaultdict(int)
    while t < 100_000:
        pos.clear()
        for robot in robots:
            x = (robot.x + t * robot.vx) % W
            y = (robot.y + t * robot.vy) % H
            pos[(x, y)] += 1
        # count neighbours
        neighbours: defaultdict[int, int] = defaultdict(int)
        for p in pos:
            n = -1
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if (p[0] + x, p[1] + y) in pos:
                        n += 1
            neighbours[n] += 1
        if neighbours[8] != 0:
            pretty_print_pos(pos, False)
            answer = input(f"Time {t}. Press q<Enter> to quit").lower()
            if answer == "q": break

        t += 1

    print(f"Answer for 14.2 is {t}")
