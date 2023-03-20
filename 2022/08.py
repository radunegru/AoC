from dataclasses import dataclass
from typing import Iterator


@dataclass
class Tree:
    height: int
    visibility: int


def read_trees(lines: Iterator[str]) -> list[list[Tree]]:
    trees = []
    for line in lines:
        trees.append([Tree(int(c), 0) for c in line.strip()])
    return trees


def part1(lines: Iterator[str]) -> None:
    trees = read_trees(lines)
    # left->right
    visibility = 8
    for row in range(len(trees)):
        max_height = -1
        for column in range(len(trees[0])):
            tree = trees[row][column]
            if tree.height > max_height:
                tree.visibility = tree.visibility | visibility
                max_height = tree.height
    # right->left
    visibility = 2
    for row in range(len(trees)):
        max_height = -1
        for column in reversed(range(len(trees[0]))):
            tree = trees[row][column]
            if tree.height > max_height:
                tree.visibility = tree.visibility | visibility
                max_height = tree.height
    # top->bottom
    visibility = 4
    for column in range(len(trees[1])):
        max_height = -1
        for row in range(len(trees)):
            tree = trees[row][column]
            if tree.height > max_height:
                tree.visibility = tree.visibility | visibility
                max_height = tree.height
    # bottom->top
    visibility = 1
    for column in range(len(trees[1])):
        max_height = -1
        for row in reversed(range(len(trees))):
            tree = trees[row][column]
            if tree.height > max_height:
                tree.visibility = tree.visibility | visibility
                max_height = tree.height

    count = 0
    for row in trees:
        count += len([tree for tree in row if tree.visibility != 0])
    print(f"Answser for 8.1 is {count}")


def part2(lines: Iterator[str]) -> None:
    trees = read_trees(lines)
    max_scenic_score = 0
    for row in range(1, len(trees) - 1):
        for column in range(1, len(trees[row]) - 1):
            scenic_score = 1
            # to left
            height = trees[row][column].height
            c = column  # to avoid pyright warning when computing scenic_score
            for c in reversed(range(0, column)):
                if trees[row][c].height >= height:
                    break
            scenic_score *= (column - c)
            # up
            r = row     # to avoid pyright warning when computing scenic_score
            for r in reversed(range(0, row)):
                if trees[r][column].height >= height:
                    break
            scenic_score *= (row - r)
            # to right
            for c in range(column + 1, len(trees[row])):
                if trees[row][c].height >= height:
                    break
            scenic_score *= (c - column)
            # down
            for r in range(row + 1, len(trees)):
                if trees[r][column].height >= height:
                    break
            scenic_score *= (r - row)
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    print(f"Answser for 8.2 is {max_scenic_score}")


