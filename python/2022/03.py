from typing import Iterator


def priority(item_type: str) -> int:
    result: int = ord(item_type) - ord("a") + 1
    if result < 0:
        result += 58
    return result


def part1(lines: Iterator[str]) -> None:
    sum_priority: int = 0
    for line in lines:
        half1: set[str] = set(line[: len(line) // 2])
        half2: set[str] = set(line[len(line) // 2 :])
        common_types: set[str] = set.intersection(half1, half2)
        if len(common_types) > 1:
            raise ValueError("More than one common type")
        sum_priority += priority(next(iter(common_types)))
    print(f"sum of priorities is {sum_priority}")
    print("</end>")


def part2(lines: Iterator[str]) -> None:
    sum_priority: int = 0
    group: list[set[str]] = []
    for line in lines:
        group.append(set(line))
        if len(group) == 3:
            common_types: set[str] = set.intersection(*group)
            if len(common_types) > 1:
                raise ValueError("More than one common type")
            print(f"{common_types=}")
            sum_priority += priority(next(iter(common_types)))
            group: list[set[str]] = []
    print(f"sum of priorities is {sum_priority}")
    print("</end>")
