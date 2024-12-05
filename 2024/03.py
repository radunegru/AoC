from typing import Iterator
import re


def part1(lines: Iterator[str]) -> None:
    result = 0
    re_mul = r"mul\((?P<f1>\d+),(?P<f2>\d+)\)"
    # lines = [
    #     "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    # ]
    for line in lines:
        matches = re.finditer(re_mul, line)
        for match in matches:
            result += int(match.group("f1")) * int(match.group("f2"))
    print(f"Answer for 3.1 in {result}")


def part2(lines: Iterator[str]) -> None:
    result = 0
    enabled = True
    re_mul = r"mul\((?P<f1>\d+),(?P<f2>\d+)\)|(do\(\))|(don't\(\))"
    # lines = [
    #     "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))+"
    # ]
    for line in lines:
        matches = re.finditer(re_mul, line)
        for match in matches:
            match match.group():
                case "do()":
                    enabled = True
                case "don't()":
                    enabled = False
                case _:
                    if enabled:
                        result += int(match.group("f1")) * int(match.group("f2"))
    print(f"Answer for 3.2 in {result}")
