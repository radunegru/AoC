from typing import Iterator
import re


def solve(lines: Iterator[str], reverse: bool) -> None:
    in_crates: bool = True  # True for reading crates, False for reading instructions
    c_stacks: int = 0
    stacks: list[list[str]] = []
    for line in lines:
        if in_crates:
            if line[1:2] == "1":
                in_crates: bool = False
            if c_stacks == 0:
                c_stacks: int = len(line) // 4
                print(f"{c_stacks=}")
                stacks: list[list[str]] = [[] for _ in range(c_stacks)]
            for i in range(c_stacks):
                crate: str = line[i * 4 + 1 : i * 4 + 2]
                if len(crate.strip()) > 0:
                    stacks[i].insert(0, crate)
        else:  # instructions
            if len(line.rstrip()) == 0:
                continue
            number_of_crates, from_stack, to_stack = map(int, re.findall(r"\d+", line))
            from_stack -= 1
            to_stack -= 1
            crates_to_move: list[str] = stacks[from_stack][-number_of_crates:]
            if reverse:
                crates_to_move.reverse()
            stacks[to_stack].extend(crates_to_move)
            stacks[from_stack] = stacks[from_stack][:-number_of_crates]
    [print(stack[-1], end="") for stack in stacks]


def part1(lines: Iterator[str]) -> None:
    solve(lines, True)


def part2(lines: Iterator[str]) -> None:
    solve(lines, False)
