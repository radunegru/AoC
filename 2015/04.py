import hashlib
from typing import Iterator


def get_key(secret_key: str, pattern: str) -> None:
    answer = 0
    while True:
        key = secret_key + str(answer)
        the_hash = hashlib.md5(key.encode("UTF-8")).hexdigest()
        if the_hash.startswith(pattern):
            return answer
        answer += 1


def part1(lines: Iterator[str]) -> None:
    answer = 0
    for line in lines:
        # line = "abcdef"
        # line = "pqrstuv"
        line = line.replace("\n", "")
        answer = get_key(line, "00000")
    print(f"Answer for 4.1 is {answer}")


def part2(lines: Iterator[str]) -> None:
    answer = 0
    for line in lines:
        # line = "abcdef"
        # line = "pqrstuv"
        line = line.replace("\n", "")
        answer = get_key(line, "000000")
    print(f"Answer for 4.1 is {answer}")
