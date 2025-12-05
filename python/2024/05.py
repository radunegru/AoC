import os
from typing import Iterator


def check_line(line, orders) -> tuple[bool, int]:
    pages = line.split(",")
    previous_page = None
    for page in pages:
        if previous_page is None:
            previous_page = page
            continue
        order_to_check = f"{previous_page}|{page}"
        if order_to_check not in orders:
            return False, 0
        previous_page = page
    else:
        if len(pages) % 2 == 1:
            return True, int(pages[int(len(pages)/2)])
        else:
            raise Exception(f"{line} is valid but contains even pages {len(pages)}")


def part1(lines: Iterator[str]) -> None:
    result = 0
    i_phase = 0
    orders: set[str] = set()
    for line in lines:
        line = line.rstrip(os.linesep)
        if line == "":
            i_phase += 1
            continue
        match i_phase:
            case 0:
                orders.add(line)
            case 1:
                line_ok, value = check_line(line, orders)
                if line_ok:
                    result += value
            case 2:
                raise Exception(f"wtf {i_phase=}")

    print(f"Answer for 5.1 is {result}")


def part2(lines: Iterator[str]) -> None:
    result = 0
    i_phase = 0
    orders: set[str] = set()
    c_line = 0
    for line in lines:
        line = line.rstrip(os.linesep)
        c_line += 1
        if line == "":
            i_phase = 1
            continue
        match i_phase:
            case 0:
                orders.add(line)
            case 1:
                if check_line(line, orders)[0]:
                    continue
                pages = line.split(",")
                print_orders: dict[str, int] = {}
                while len(pages) > 1:
                    page1 = pages.pop()
                    if page1 not in print_orders:
                        print_orders[page1] = 0
                    for page2 in pages:
                        if page2 not in print_orders:
                            print_orders[page2] = 0
                        if f"{page1}|{page2}" in orders:
                            c_page = print_orders.get(page1, 0)
                            print_orders[page1] = c_page + 1
                        elif f"{page2}|{page1}" in orders:
                            c_page = print_orders.get(page2, 0)
                            print_orders[page2] = c_page + 1
                        else:
                            print(f"    {page1} -- {page2} not found")
                inv_dict = { count: page for page, count in print_orders.items() }
                good_order = [ page for _, page in sorted(inv_dict.items(), reverse=True) ]
                pages = line.split(",")
                line_ok, value = check_line(",".join(good_order), orders)
                if line_ok:
                    result += value
                else:
                    print(f"{good_order} not good (line {line})")
            case 2:
                raise Exception(f"wtf {i_phase=}")
    print(f"Answer for 5.2 is {result}")
