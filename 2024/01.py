from typing import Iterator


def get_lists(lines: Iterator[str]) -> tuple[list[int], list[int]]:
    list1: list[int] = []
    list2: list[int] = []
    for line in lines:
        item1, item2 = tuple(line.split())
        list1.append(int(item1))
        list2.append(int(item2))

    return list1, list2


def part1(lines: Iterator[str]) -> None:
    list1, list2 = get_lists(lines)
    list1.sort()
    list2.sort()

    sum: int = 0
    for item1, item2 in zip(list1, list2):
        sum+= abs(item1 - item2)
    print(f"Answer for 2024.1.1 is {sum}")


def part2(lines: Iterator[str]) -> None:
    list1, list2 = get_lists(lines)
    score: dict[int, int] = {}
    for item2 in list2:
        item_score = score.get(item2, 0)
        score[item2] = item_score + 1

    similarity_score: int = 0
    for item1 in list1:
        similarity_score += item1 * score.get(item1, 0)

    print(f"Answer for 2024.1.2 is {similarity_score}")
