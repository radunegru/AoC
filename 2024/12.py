from dataclasses import dataclass, field
import os
from typing import Iterator


from shape_angles import Shape


ALL_SHAPES: dict[int, Shape] = {}
TERRAIN_SIZE: int = 0


def neighbour_iterator(y: int, x: int) -> Iterator[tuple[int, int]]:
    yield (y, x + 1) # right
    yield (y + 1, x) # down
    yield (y, x - 1) # left
    yield (y - 1, x) # up


def safe_neighbour(terrain: list[str], y: int, x: int):
    if (0 <= x < TERRAIN_SIZE) and (0 <= y < TERRAIN_SIZE):
        return terrain[y][x]
    return "."


def neighbours(terrain: list[str], plot: str, y: int, x: int) -> int:
    global TERRAIN_SIZE
    c_neighbours = 0
    for new_y, new_x in neighbour_iterator(y, x):
        c_neighbours += 1 if safe_neighbour(terrain, new_y, new_x) != plot else 0
    return c_neighbours


def explore_region(terrain: list[str], visited: set[tuple[int, int]], region: str, y: int, x: int) -> tuple[int, int]:
    area = 1
    perimeter = neighbours(terrain, region, y, x)
    visited.add((y, x))
    for new_y, new_x in neighbour_iterator(y, x):
        if (new_y, new_x) in visited:
            continue
        candidate_plot = safe_neighbour(terrain, new_y, new_x)
        if candidate_plot == region:
            candidate_area, candidate_perimeter = explore_region(terrain, visited, region, new_y, new_x)
            area += candidate_area
            perimeter += candidate_perimeter

    return (area, perimeter)


def get_shape_for_point(terrain: list[str], y: int, x: int) -> Shape:
    l_shape_id: list[str] = []
    plot = terrain[y][x]
    for delta_y in range(-1, 2):
        for delta_x in range(-1, 2):
            if (delta_y == 0) and (delta_x == 0): continue
            neighbour = safe_neighbour(terrain, y + delta_y, x + delta_x)
            l_shape_id.append("1" if neighbour == plot else "0")
    shape_id: int = int("".join(l_shape_id), 2)
    # if plot == "S":
    #     print(f"{shape_id=}")
    return ALL_SHAPES[int("".join(l_shape_id), 2)]


def explore_region2(terrain: list[str], visited: set[tuple[int, int]], region: str, y: int, x: int) -> tuple[int, int]:
    area = 1
    angles = get_shape_for_point(terrain, y, x).angles
    # if region == "S":
    #     print(f"Angles for {y=}, {x=} = {angles}")
    visited.add((y, x))
    for new_y, new_x in neighbour_iterator(y, x):
        if (new_y, new_x) in visited:
            continue
        candidate_plot = safe_neighbour(terrain, new_y, new_x)
        if candidate_plot == region:
            candidate_area, candidate_angles = explore_region2(terrain, visited, region, new_y, new_x)
            area += candidate_area
            angles += candidate_angles

    return (area, angles)


def part1(lines: Iterator[str]) -> None:
    global TERRAIN_SIZE

    terrain: list[str] = [line.rstrip(os.linesep) for line in lines]
    TERRAIN_SIZE = len(terrain)
    visited: set[tuple[int, int]] = set()
    region = "."
    price = 0
    for y, row in enumerate(terrain):
        for x, plot in enumerate(row):
            if (y, x) in visited:
                continue
            if region == ".":
                region = plot
                area, perimeter = explore_region(terrain, visited, region, y, x)
                # print(f"region {region}: {area=}, {perimeter=}")
                price += area * perimeter
            region = "."

    print(f"Answer for 12.1 is {price}")


def part2(lines: Iterator[str]) -> None:
    global ALL_SHAPES, TERRAIN_SIZE

    with open("./shapes.json", "r") as fp:
        ALL_SHAPES = Shape.deserialize_all_shapes(fp)

    terrain: list[str] = [line.rstrip(os.linesep) for line in lines]
    TERRAIN_SIZE = len(terrain)
    visited: set[tuple[int, int]] = set()
    region = "."
    price = 0
    for y, row in enumerate(terrain):
        for x, plot in enumerate(row):
            if (y, x) in visited:
                continue
            if region == ".":
                region = plot
                area, sizes = explore_region2(terrain, visited, region, y, x)
                # print(f"A region of {region} plants with {area=} * {sizes=}")
                price += area * sizes
            region = "."

    print(f"Answer for 12.1 is {price}")
    # configs: set[str] = set()
    # for y, row in enumerate(terrain):
    #     for x, plot in enumerate(row):
    #         config: list[str] = []
    #         for delta_y in range(-1, 2):
    #             for delta_x in range(-1, 2):
    #                 neighbour = safe_neighbour(terrain, y + delta_y, x + delta_x)
    #                 config.append("a" if neighbour == plot else ".")
    #         configs.add("".join(config))
    # for i, c in enumerate(sorted(list(configs))):
    #     print(c)
    # print(len(configs))
    # get_shape_for_point(terrain, 0, 0)
