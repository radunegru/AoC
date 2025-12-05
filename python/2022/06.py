from typing import Iterator


def check_preamble(lines: Iterator[str], length: int) -> None:
    for line in lines:
        message:str = line.strip()
        preamble: list[str] = []
        for i, c in enumerate(message, 1):
            preamble.append(c)
            if len(preamble) < length:
                continue
            if len(set(preamble)) == length:
                print(f"message starts at {i}")
                break
            preamble.pop(0)
        break


def part1(lines: Iterator[str]) -> None:
    check_preamble(lines, 4)


def part2(lines: Iterator[str]) -> None:
    check_preamble(lines, 14)


