from typing import Iterator


def check_report(report: list[str]) -> tuple[bool, int]:
    """Checks a report and returns:
    (True, -1) - if the report is good
    (False, position) - if the report is not good. The Problem Dampener can
        be applied of item at the returned position, or the next item
    """
    position = 0
    item1: int | None = None
    order: bool | None = None # None not initialized, False DESC, True ASC
    for item2 in report:
        if item1 is None:
            item1 = int(item2)
            continue
        item2 = int(item2)
        if not 0 < abs(item1 - item2) < 4:
            return False, position
        if order is None:
            order = item1 < item2
        elif order != (item1 < item2):
            return False, position
        item1 = item2
        position += 1
    return True, -1


def print_report(report: list[str], is_good: bool, position: int) -> None:
    if is_good:
        print("\u2705", end="")
    else:
        print("\u274c", end="")
    for i in range(0, len(report)):
        if i == position:
            if is_good:
                print("\N{esc}[35m", end="")
            else:
                print("\N{esc}[31m", end="")
        print(f" {report[i]}", end="")
        if i == position:
            print("\N{esc}[0m", end="")
    print()


def part1(lines: Iterator[str]) -> None:
    count: int = 0
    for line in lines:
        report = line.split()
        is_good, position = check_report(report)
        if is_good:
            count += 1
        print_report(report, is_good, position)

    print(f"Answer for 2.1 is {count}")


def part2(lines: Iterator[str]) -> None:
    count: int = 0
    for line in lines:
        report = line.split()
        is_good, position = check_report(report)
        if is_good:
            count += 1
            print_report(report, True, -1)
            continue

        report1 = line.split()
        report1.pop(position)
        if check_report(report1)[0]:
            count += 1
            print_report(report, True, position)
            continue
        report2 = line.split()
        report2.pop(position + 1)
        if check_report(report2)[0]:
            count += 1
            print_report(report, True, position + 1)
            continue
        report3 = line.split()
        report3.pop(0)
        if check_report(report3)[0]:
            count += 1
            print_report(report, True, 0)
            continue
        print_report(report, False, position)

    print(f"Answer for 2.1 is {count}")
