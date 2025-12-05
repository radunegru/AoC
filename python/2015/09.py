from itertools import permutations
from typing import Iterator
import sys


def held_karp(mask: int, pos: int, n: int, cost:list[list[int]]) -> int:
    """
    https://www.geeksforgeeks.org/travelling-salesman-problem-using-dynamic-programming/
    """
    # Base case: if all cities are visited, return the cost to return to the
    # starting city
    if mask == (1 << n) -1:
        # return cost[pos][0]
        return 0

    result = sys.maxsize

    # Try visiting every city that has not been visited yet
    for i in range(n):
        if (mask & (1 << i)) == 0:
            # City is not visited. Visit it and update the mask
            result = min(
                result,
                cost[pos][i] + held_karp(mask | (1 << i), i, n, cost))

    return result


def pretty_print(vertices: dict[str, int], distances: list[list[int]]) -> None:
    max_name = max([len(name) for name in vertices.keys()])
    for i in range(max_name):
        line = " " * max_name
        for dest, _ in vertices.items():
            if i < len(dest):
                line = f"{line}   {dest[i]}"
            else:
                line = f"{line}    "
        print(line)

    for start, i_start in vertices.items():
        line = f"{start:{max_name}}"
        for _, i_dest in vertices.items():
            line = f"{line} {distances[i_start][i_dest]:3}"
        print(line)


def part1_old(lines: Iterator[str]) -> None:
    # memo = [[-1] * (1 << (n + 1)) for _ in range(n + 1)]
    vertices: dict[str, int] = {}
    temp_distances: dict[str, dict[str, int]] = {}
    for line in lines:
        start, _, dest, _, distance = line.split()
        distance = int(distance)
        if start not in vertices:
            vertices[start] = len(vertices)
            temp_distances[start] = {}
            temp_distances[start][start] = 0
        if dest not in vertices:
            vertices[dest] = len(vertices)
            temp_distances[dest] = {}
            temp_distances[dest][dest] = 0
        temp_distances[start][dest] = distance
        temp_distances[dest][start] = distance

    n = len(vertices) # the number of vertices
    distances: list[list[int]] = [[0] * n for _ in range(n)]
    for start, data in temp_distances.items():
        for dest, distance in data.items():
            distances[vertices[start]][vertices[dest]] = distance
    pretty_print(vertices, distances)

    result = held_karp(1, 0, len(vertices), distances)
    print(f"Answer to 9.1 is {result}")


def part1(lines: Iterator[str]) -> None:
    places = set()
    distances = dict()
    for line in lines:
        source, _, dest, _, distance = line.split()
        distance = int(distance)
        places.add(source)
        places.add(dest)
        distances.setdefault(source, dict())[dest] = distance
        distances.setdefault(dest, dict())[source] = distance

    shortest = sys.maxsize
    longest = 0
    for items in permutations(places):
        dist = sum(map(lambda x, y: distances[x][y], items[:-1], items[1:]))
        shortest = min(shortest, dist)
        longest = max(longest, dist)

    print(f"Anwser for 9.1 is {shortest}")
    print(f"Anwser for 9.2 is {longest}")


def part2(lines: Iterator[str]) -> None:
    part1(lines)
