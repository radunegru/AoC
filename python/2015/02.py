from typing import Iterator


def part1(lines: Iterator[str]) -> None:
    paper = 0
    for line in lines:
        dimensions = [int(dimension) for dimension in line.split("x")]
        areas: list[int] = []
        for i in range(0, len(dimensions) - 1):
            for j in range(i + 1, len(dimensions)):
                areas.append(dimensions[i] * dimensions[j])
        paper += min(areas) + 2 * sum(areas)
    print(f"Answer for 2.1 is {paper}")


def part2(lines: Iterator[str]) -> None:
    ribbon = 0
    for line in lines:
        dimensions = [int(dimension) for dimension in line.split("x")]
        perimeters: list[int] = []
        for i in range(0, len(dimensions) - 1):
            for j in range(i + 1, len(dimensions)):
                perimeters.append(2 * dimensions[i] + 2 * dimensions[j])
        volume = 1
        for dimension in dimensions:
            volume *= dimension
        ribbon += volume + min(perimeters)
        # print(f"{line=}, {perimeters=}, {volume=}, {ribbon=}")
    print(f"Answer for 2.2 is {ribbon}")
