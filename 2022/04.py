from typing import Iterator


def compute_region(lines: Iterator[str], style) -> int:
    result: int = 0
    for line in lines:
        sectors: list[str] = line.split(",")
        a1f, a1l = map(int, sectors[0].split("-"))
        a2f, a2l = map(int, sectors[1].split("-"))
        result += style(a1f, a1l, a2f, a2l)
    return result


def part1(lines: Iterator[str]) -> None:
    contained_pairs: int = compute_region(lines, lambda a1f, a1l, a2f, a2l: 1 if (a1f <= a2f) and (a1l >= a2l) else 1 if (a1f >= a2f) and (a1l <= a2l) else 0)
    print(f"There are {contained_pairs} pairs")


def part2(lines: Iterator[str]) -> None:
    overlapped: int = compute_region(lines, lambda a1f, a1l, a2f, a2l: 1 if (a2f <= a1f <= a2l) or (a2f <= a1l <= a2l) or (a1f <= a2f <= a1l) or (a1l <= a2l <= a1l) else 0)
    print(f"There are {overlapped} overlapped pairs")
