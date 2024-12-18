import re
from typing import Iterator


def part1(lines: Iterator[str]) -> None:
    re_a = r"^Button A: X\+(?P<a1>\d+), Y\+(?P<a2>\d+)$"
    re_b = r"^Button B: X\+(?P<b1>\d+), Y\+(?P<b2>\d+)$"
    re_prize = r"^Prize: X=(?P<X>\d+), Y=(?P<Y>\d+)$"
    it_lines = iter(lines)
    cost:int = 0
    try:
        while True:
            a = next(it_lines)
            m = re.match(re_a, a)
            a1 = int(m.group("a1")); a2 = int(m.group("a2"))
            b = next(it_lines)
            m = re.match(re_b, b)
            b1 = int(m.group("b1")); b2 = int(m.group("b2"))
            p = next(it_lines)
            m = re.match(re_prize, p)
            X = int(m.group("X")); Y = int(m.group("Y"))
            B = (Y * a1 - X * a2) / (a1 * b2 - a2 * b1)
            A = (X - b1 * B) / a1
            if B.is_integer() and A.is_integer():
                cost += int(A * 3 + B)
                print(f"Push A {A} times, push B {B} times, cost {A * 3 + B}")

            next(it_lines)
    except StopIteration:
        pass

    print(f"Answer for 13.1 is {cost}")


def part2(lines: Iterator[str]) -> None:
    re_a = r"^Button A: X\+(?P<a1>\d+), Y\+(?P<a2>\d+)$"
    re_b = r"^Button B: X\+(?P<b1>\d+), Y\+(?P<b2>\d+)$"
    re_prize = r"^Prize: X=(?P<X>\d+), Y=(?P<Y>\d+)$"
    it_lines = iter(lines)
    cost:int = 0
    try:
        while True:
            a = next(it_lines)
            m = re.match(re_a, a)
            a1 = int(m.group("a1")); a2 = int(m.group("a2"))
            b = next(it_lines)
            m = re.match(re_b, b)
            b1 = int(m.group("b1")); b2 = int(m.group("b2"))
            p = next(it_lines)
            m = re.match(re_prize, p)
            X = int(m.group("X")) + 10000000000000
            Y = int(m.group("Y")) + 10000000000000
            B = (Y * a1 - X * a2) / (a1 * b2 - a2 * b1)
            A = (X - b1 * B) / a1
            if B.is_integer() and A.is_integer():
                cost += int(A * 3 + B)
                print(f"Push A {A} times, push B {B} times, cost {A * 3 + B}")

            next(it_lines)
    except StopIteration:
        pass

    print(f"Answer for 13.2 is {cost}")
