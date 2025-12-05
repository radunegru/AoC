import os
from typing import Iterator


def rec1(target:int, compute: int, terms: list[int], current: int) -> bool:
    if current == len(terms):
        if compute == target:
            return True
        else:
            return False
    intermediate = compute * terms[current]
    if intermediate <= target:
        if rec1(target, intermediate, terms, current + 1):
            return True
    intermediate = compute + terms[current]
    if intermediate > target:
        return False
    else:
        return rec1(target, intermediate, terms, current + 1)


def rec2(target:int, compute: int, terms: list[int], current: int) -> bool:
    if current == len(terms):
        if compute == target:
            return True
        else:
            return False
    intermediate = compute * terms[current]
    if intermediate <= target:
        if rec2(target, intermediate, terms, current + 1):
            return True
    intermediate = compute + terms[current]
    if intermediate <= target:
        if rec2(target, intermediate, terms, current + 1):
            return True
    intermediate = int(str(compute) + str(terms[current]))
    if intermediate > target:
        return False
    else:
        return rec2(target, intermediate, terms, current + 1)


def part2(lines: Iterator[str]) -> None:
    answer = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        result, operands = line.split(": ")
        result = int(result)
        terms = [int(operand) for operand in operands.split(" ")]
        if rec2(result, terms[0], terms, 1):
            answer += result

    print(f"Answer for 7.2 is {answer}")
