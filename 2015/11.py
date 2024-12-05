import os
from typing import Iterator


rule2_set = set("iol")


def check_password(password: str) -> bool:
    # rule 1
    ord_last_char = None
    c_increasing = 0
    b_rule1 = False
    for c in password:
        if ord_last_char is None:
            ord_last_char = ord(c)
            continue
        if ord(c) - ord_last_char == 1:
            c_increasing += 1
            if c_increasing == 2:
                b_rule1 = True
                break
        else:
            c_increasing = 0
        ord_last_char = ord(c)
    if not b_rule1:
        return False

    # rule 2
    password_set = set(password)
    if not rule2_set.isdisjoint(password_set):
        return False

    #rule 3
    last_char = None
    pairs = set()
    b_rule3 = False
    for c in password:
        if last_char and (c == last_char):
            pairs.add(c)
            if len(pairs) == 2:
                b_rule3 = True
                break
            last_char = None
            continue
        last_char = c
    return b_rule3


def next_old_password(password: str) -> str:
    w = password[::-1]
    result = []
    carry = True
    for c in w:
        if carry:
            if c == "z":
                result.append("a")
                continue
            result.append(chr(ord(c) + 1))
            carry = False
        else:
            result.append(c)
    return "".join(result)[::-1]


def next_good_password(password: str) -> str:
    while(True):
        password = next_old_password(password)
        if check_password(password):
            return password


def part1(lines: Iterator[str]) -> None:
    new_password = None
    for line in lines:
        line = line.rstrip(os.linesep)
        new_password = next_good_password(line)

    print(f"Answer for 11.1 is {new_password}")


def part2(lines: Iterator[str]) -> None:
    new_password = None
    for line in lines:
        line = line.rstrip(os.linesep)
        new_password = next_good_password(line)
        new_password = next_good_password(new_password)

    print(f"Answer for 11.2 is {new_password}")
