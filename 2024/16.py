from collections import defaultdict, deque
import curses
from enum import IntEnum
import os
from typing import Iterator, Optional


# class Node:
#     _directions = [
#         ( 0, +1), # right
#         (+1,  0), # down
#         ( 0, -1), # left
#         (-1,  0)  # up
#     ]

#     def __init__(self, x: int, y: int, direction: tuple[int, int], score: int) -> None:
#         self.x = x; self.y = y
#         self.direction = direction
#         self.score = score

#     def follow(self) -> Iterator["Node"]:
#         yield Node(
#             self.x + self.direction[1],
#             self.y + self.direction[0],
#             self.direction,
#             self.score + 1
#         )
#         new_dir = self._directions[(self._directions.index(self.direction) + 1 + 4) % 4]
#         yield Node(
#             self.x + new_dir[1],
#             self.y + new_dir[0],
#             new_dir,
#             self.score + 1001
#         )
#         new_dir = self._directions[(self._directions.index(self.direction) - 1 + 4) % 4]
#         yield Node(
#             self.x + new_dir[1],
#             self.y + new_dir[0],
#             new_dir,
#             self.score + 1001
#         )


# def part1(lines: Iterator[str]) -> None:
#     score = 0

#     maze: list[list[str | int]] = []
#     start: tuple[int, int] = (-1, -1)
#     end: tuple[int, int] = (-1, -1)
#     for y, line in enumerate(lines):
#         row: list[str | int] = []
#         for x, c in enumerate(line.rstrip(os.linesep)):
#             match c:
#                 case "S":
#                     start = (y, x)
#                     c = "."
#                 case "E":
#                     end = (y, x)
#                     c = "."
#             row.append(c)
#         maze.append(row)

#     q: deque[Node] = deque()
#     q.append(Node(start[1], start[0], (0, 1), 0))
#     maze[start[0]][start[1]] = 0

#     while len(q) > 0:
#         node = q.popleft()
#         for next_node in node.follow():
#             cell = maze[next_node.y][next_node.x]
#             if cell == "#":
#                 continue
#             if (cell == ".") or (isinstance(cell, int) and (cell > next_node.score)):
#                 maze[next_node.y][next_node.x] = next_node.score
#                 q.append(next_node)
#     # for row in maze:
#     #     for cell in row:
#     #         print(f"{cell} ", end="")
#     #     print()
#     score = maze[end[0]][end[1]]

#     print(f"Answer for 16.1 is {score}")


class Direction(IntEnum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3


class Node:
    delta_y: list[int] = [  0, +1,  0, -1 ]
    delta_x: list[int] = [ +1,  0, -1,  0 ]
    def __init__(self, y: int, x: int, direction: Direction, score: int) -> None:
        self.y = y; self.x = x
        self.direction = direction
        self.score = score
        self.parent: Optional["Node"] = None

    def init_next_nodes(self) -> None:
        self.next_nodes = [ n for n in self.follow() ]

    def follow(self) -> Iterator["Node"]:
        # same direction
        dy = Node.delta_y[int(self.direction)]; dx = Node.delta_x[int(self.direction)]
        yield Node(self.y + dy, self.x + dx, self.direction, self.score + 1)
        # turn right
        i: int = (int(self.direction) + 1 + 4) % 4
        dy = Node.delta_y[i]; dx = Node.delta_x[i]
        yield Node(self.y + dy, self.x + dx, Direction(i), self.score + 1001)
        # turn left
        i = (int(self.direction) - 1 + 4) % 4
        dy = Node.delta_y[i]; dx = Node.delta_x[i]
        yield Node(self.y + dy, self.x + dx, Direction(i), self.score + 1001)

    def __repr__(self) -> str:
        return f"({self.y}, {self.x}) {['>', 'v', '<', '^'][self.direction]} {self.score}"


maze: list[list[str]] = []
start: tuple[int, int] = (-1, -1)
end: tuple[int, int] = (-1, -1)
current_path: list[Node] = []
solutions: defaultdict[int, list[list[Node]]] = defaultdict(list)
# visited: set[tuple[int, int]] = set()


def is_node_in_current_path(n: Node) -> bool:
    global current_path
    for node in current_path:
        if (n.y == node.y) and (n.x == node.x):
            return True
    return False


def point_in_current_path(y: int, x: int) -> Optional[Node]:
    global current_path
    for node in current_path:
        if (y == node.y) and (x == node.x):
            return node
    return None


def bfs_recursive(n: Node) -> None:
    global maze, start, end, current_path, solutions
    current_path.append(n)
    if (n.y, n.x) == end:
        # found a solution
        solutions[n.score].append(current_path.copy())
        print(f"Solution {len(solutions)} ({n.score})")
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                nn: Optional[Node] = point_in_current_path(y, x)
                if nn is not None:
                    cell = [">", "v", "<", "^"][nn.direction]
                print(cell, end="")
            print()
        # print(current_path)
        # print("    ", n.score)
    else:
        for new_node in n.follow():
            # print(new_node, end="")
            if maze[new_node.y][new_node.x] != ".":
                # print("wall")
                continue
            if is_node_in_current_path(new_node):
                # print("already visited")
                continue
            bfs_recursive(new_node)
    current_path.pop()


def bfs_non_recursive_0(maze: list[list[str]], start: tuple[int, int], end: tuple[int, int]) -> None:
    current_node = Node(start[0], start[1], Direction.Right, 0)
    current_node.init_next_nodes()
    min_score = len(maze) * len(maze) * 1000
    min_score = 65437
    print(f"{min_score=}")
    while current_node is not None:
        if len(current_node.next_nodes) > 0:
            next_node = current_node.next_nodes.pop()
            if (next_node.y == end[0]) and (next_node.x == end[1]):
                if next_node.score < min_score:
                    solutions.clear()
                    print(f"new min score {next_node.score}")
                if next_node.score <= min_score:
                    min_score = next_node.score
                    solutions[min_score].append(current_path.copy())
            elif (
                (next_node.score <= min_score)
                and (maze[next_node.y][next_node.x] == ".")
                and not is_node_in_current_path(next_node)
                ):
                next_node.init_next_nodes()
                current_path.append(next_node)
                current_node = next_node
                # continue
            else: # wall, ignore node
                pass
        else: # no more next nodes for current node
            if len(current_path) > 0:
                current_node = current_path.pop()
            else:
                current_node = None


def read_data(lines: Iterator[str]) -> None:
    global maze, start, end
    for y, line in enumerate(lines):
        row: list[str] = []
        for x, cell in enumerate(line):
            match cell:
                case "S":
                    start = (y, x)
                    cell = "."
                case "E":
                    end = (y, x)
                    cell = "."
                case "#" | ".":
                    pass
                case _:
                    continue
            row.append(cell)
        maze.append(row)


def bfs_non_recursive(maze: list[list[str]], start: tuple[int, int], end: tuple[int, int]) -> None:
    q: deque[Node] = deque()
    explored: set[tuple[int, int]] = { start }
    print(f"{start in explored}")
    q.append(Node(start[0], start[1], Direction.Right, 0))
    while len(q) > 0:
        current_node = q.popleft()
        if (current_node.y, current_node.x) == end:
            copy_maze = [ [ cell for cell in row ] for row in maze ]
            cn = current_node
            while cn.parent is not None:
                copy_maze[cn.y][cn.x] = [">", "v", "<", "^"][int(cn.direction)]
                # print(f"    ({cn.y}, {cn.x}, {cn.score})", end="")
                cn = cn.parent
            # print()
            # print(f"Found path score {current_node.score} ({len(q)=})")
            # print(f"{end=}, ({current_node.y, current_node.x})")
            copy_maze[start[0]][start[1]] = "S"
            copy_maze[end[0]][end[1]] = "E"
            for row in copy_maze:
                for cell in row:
                    print(cell, end="")
                print()
            print("q is")
            for node in q:
                print(f"    {node}")
            continue
        for next_node in current_node.follow():
            if maze[next_node.y][next_node.x] == "#": continue
            if (next_node.y, next_node.x) not in explored:
                explored.add((next_node.y, next_node.x))
                next_node.parent = current_node
                q.append(next_node)


def part1(lines: Iterator[str]) -> None:
    read_data(lines)

    c_dot = 0
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == ".": c_dot += 1
            if (y, x) == start:
                cell = "S"
            elif (y, x) == end:
                cell = "E"
            print(cell, end="")
        print()
    print(f"{start=}, {end=} ({c_dot=})")

    # start_node = Node(start[0], start[1], Direction.Right, 0)
    # bfs_recursive(start_node)
    bfs_non_recursive(maze, start, end)
    # for k in sorted(solutions.keys()):
    #     print(f"{k} -- {len(solutions[k])}")

    score = 0
    # score = min(solutions.keys())
    print(f"Answer for 16.1 is {score}")
