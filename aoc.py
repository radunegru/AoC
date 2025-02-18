"""
Dynamically import specified day and execute solver.

Info on dynamically loading files in [How do I dynamically import all *.py files from a given directory AND all sub-directories?](https://stackoverflow.com/questions/57878744/how-do-i-dynamically-import-all-py-files-from-a-given-directory-and-all-sub-di)
"""
import argparse
from importlib.machinery import ModuleSpec
import importlib.util
import os
from types import ModuleType
from typing import Iterator


def get_input_lines(
        year: int,
        day: int,
        test: bool,
        suffix: str
    ) -> Iterator[str]:
    """ Iterates the lines from the input, keeping the ending newline.

    Args:
        year: The puzzle year
        day: The puzzle day
        test: Use test input, if True, or real input, if False
        suffix: Additional part in the input file name

    Returns:
        An iterator on each line in the input file.
    """
    file_name: str = os.path.join(
        f"{year}",
        f"{day:02}_{'test' if test else 'input'}{"_" if suffix else ""}{suffix}.txt"
    )
    with open(file_name, "r") as finput:
        while True:
            line: str | None = finput.readline()
            if not line:
                break
            yield line  # .rstrip(os.linesep)


def main() -> None:
    # Initialize arguments
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("year")
    parser.add_argument("day")
    parser.add_argument("part")
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-s", "--suffix", required=False, default="")

    # read arguments
    args: argparse.Namespace = parser.parse_args()
    year: int = int(args.year)
    day: int = int(args.day)
    part: int = int(args.part)
    test: bool = args.test
    suffix: str = args.suffix

    # load module for requested day
    module_file: str = os.path.join(f"{year}", f"{day:02}.py")
    module_name: str = "solver"
    module_spec: ModuleSpec | None = importlib.util.spec_from_file_location(
        module_name, module_file
    )
    if not module_spec:
        raise ModuleNotFoundError(name=module_file)
    solver: ModuleType = importlib.util.module_from_spec(module_spec)
    if module_spec.loader:
        module_spec.loader.exec_module(solver)

    # Execute solver
    match part:
        case 1:
            solver.part1(get_input_lines(year, day, test, suffix))
        case 2:
            solver.part2(get_input_lines(year, day, test, suffix))
        case _:
            raise ValueError(f"Invalid part: {part}. Valid values are 1 or 2")


if __name__ == "__main__":
    main()
