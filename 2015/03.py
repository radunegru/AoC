from typing import Iterator


def get_movement(direction: str) -> complex:
    movement = 0j
    match direction:
        case "^":
            movement = -1j
        case "v":
            movement = 1j
        case ">":
            movement = 1
        case "<":
            movement = -1
    return movement


def part1(lines: Iterator[str]) -> None:
    position = 0 + 0j
    houses = { position }
    for line in lines:
        # line = ">"
        # line = "^>v<"
        # line = "^v^v^v^v^v"
        for direction in line:
            position += get_movement(direction)
            houses.add(position)

    print(f"Answer for 3.1 is {len(houses)}")


def part2(lines: Iterator[str]) -> None:
    s_pos = 0 + 0j
    r_pos = 0 + 0j
    houses = { s_pos, r_pos }
    for line in lines:
        # line = ">"
        # line = "^>v<"
        # line = "^v^v^v^v^v"
        line_iter = iter(line)
        while True:
            try:
                # Santa's turn
                c = next(line_iter)
                s_pos += get_movement(c)
                houses.add(s_pos)
                # Robo's turn
                c = next(line_iter)
                r_pos += get_movement(c)
                houses.add(r_pos)
            except StopIteration:
                break
    print(f"Answer for 3.2 is {len(houses)}")
