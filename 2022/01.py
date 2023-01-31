from typing import Iterator


def compute_calories(lines: Iterator[str]) -> list[int]:
    calories: list[int] = []
    current_sum: int = 0
    for line in lines:
        if len(line) == 0:
            calories.append(current_sum)
            current_sum: int = 0
        else:
            current_sum += int(line)
    calories.append(current_sum)
    calories.sort(reverse=True)
    return calories


def part1(lines: Iterator[str]) -> None:
    calories: list[int] = compute_calories(lines)
    print(f"Elf with maximum calories has {calories[0]} calories")


def part2(lines: Iterator[str]) -> None:
    calories: list[int] = compute_calories(lines)
    print(f"Top 3 elves carry {sum(calories[0:3])} calories")
