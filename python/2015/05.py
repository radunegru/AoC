import re
from typing import Iterator


def part1(lines: Iterator[str]) -> None:
    c_nice_words = 0
    # lines = [
    #     "ugknbfddgicrmopn",
    #     "aaa",
    #     "jchzalrnumimnmhp",
    #     "haegwjzuvuyypxyu",
    #     "dvszwmarrgswjxmb"
    # ]
    for line in lines:
        line = line.replace("\n", "")
        c_vowels = 0
        last_char = ""
        has_letter_twice = False
        has_forbidden_string = False
        for c in line:
            if c in "aeiou":
                c_vowels += 1
            if c == last_char:
                has_letter_twice = True
            else:
                word = last_char + c
                if word in ["ab", "cd", "pq", "xy"]:
                    has_forbidden_string = True
                    break
            last_char = c
        if (c_vowels >= 3) and has_letter_twice and not has_forbidden_string:
            print(f"{line} is a nice word")
            c_nice_words += 1
        else:
            print(f"{line} is naughty")

    print(f"Answer for 5.1 is {c_nice_words}")


def part2(lines: Iterator[str]) -> None:
    c_nice_words = 0
    re_rule1 = r"(.{2}).*\1"
    re_rule2 = r"(.).\1"
    # lines = [
    #     "qjhvhtzxzqqjkmpb",
    #     "xxyxx",
    #     "uurcxstgmygtbstg",
    #     "ieodomkazucvgmuy"
    # ]
    for line in lines:
        line = line.replace("\n", "")
        m1 = re.search(re_rule1, line)
        m2 = re.search(re_rule2, line)
        if (m1 is not None) and (m2 is not None):
            c_nice_words += 1
        # print(f"{line=}, {m1=}, {m2=}")
    print(f"Answer for 5.2 is {c_nice_words}")
