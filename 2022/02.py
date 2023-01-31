from typing import Iterator


score_round: dict[str, int] = {
    "A X": 3,
    "A Y": 6,
    "A Z": 0,
    "B X": 0,
    "B Y": 3,
    "B Z": 6,
    "C X": 6,
    "C Y": 0,
    "C Z": 3,
}
score_shape: dict[str, int] = {"X": 1, "Y": 2, "Z": 3}
required_shape: dict[str, dict[str, str]] = {
    "A": {"X": "Z", "Y": "X", "Z": "Y"},
    "B": {"X": "X", "Y": "Y", "Z": "Z"},
    "C": {"X": "Y", "Y": "Z", "Z": "X"},
}


def compute_score(lines: Iterator[str], modifier) -> int:
    score: int = 0
    for line in lines:
        line: str = modifier(line)
        score += score_round[line] + score_shape[line.split()[1]]
    return score


def part1(lines: Iterator[str]) -> None:
    score: int = compute_score(lines, lambda line: line)
    print(f"Total score for part1 is {score}")


def part2(lines: Iterator[str]) -> None:
    score: int = compute_score(
        lines,
        lambda line: line.split()[0]
        + " "
        + required_shape[line.split()[0]][line.split()[1]],
    )
    print(f"Total score for part2 is {score}")
