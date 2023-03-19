import re
from typing import Iterator
import typing


# part 1
MAX_DIR_SIZE = 100000
# part 2
DISK_SIZE = 70000000
FREESPACE = 30000000


def read_dirs(lines: Iterator[str]) -> typing.Dict[str, int]:
    dirs = {}
    path = ""
    currentLine = 0
    for line in lines:
        currentLine += 1
        command = line.strip()
        if command == "$ cd /":
            path = "/"
            dirs[path] = 0
            continue
        elif command == "$ ls":
            continue    # nothing to do, wait for the result
        m = re.match(r"^\$ cd (?P<dir>.+)$", command)
        if m:
            directory = m.group("dir")
            assert("/" not in directory)
            if directory == "..":
                path = path[0:path.rfind("/", 0, -1) + 1]
            else:
                path = path + directory + "/"
                assert(dirs[path] == 0)
            continue
        m = re.match(r"^dir (?P<dir>.+)$", command)
        if m:
            directory = m.group("dir")
            assert("/" not in directory)
            dirs[path + directory + "/"] = 0
            continue
        m = re.match(r"^(?P<size>\d+) (?P<file>.+)$", command)
        if m:
            size = int(m.group("size"))
            cdirs = path.split("/")[:-1]
            cdir = ""
            for idir in cdirs:
                cdir += idir + "/"
                dirs[cdir] += size
            continue
        raise RuntimeError(f"{currentLine}: Unknown '{command}'")
    return dirs


def part1(lines: Iterator[str]) -> None:
    dirs = read_dirs(lines)
    print(f"Answer for 7.1 is {sum([ dirsize for dirsize in dirs.values() if dirsize < MAX_DIR_SIZE])}")


def part2(lines: Iterator[str]) -> None:
    dirs = read_dirs(lines)
    current_free_space = DISK_SIZE - dirs["/"]
    print(f"current free space={current_free_space}")
    min_size = DISK_SIZE
    for size in dirs.values():
        if (current_free_space + size > FREESPACE) and (size < min_size):
            min_size = size
    print(f"Answer for 7.2 is {min_size}")
