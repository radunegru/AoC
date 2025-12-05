from dataclasses import dataclass
import re
from typing import Iterator


@dataclass
class Wire:
    name: str
    input: str
    value: int = 65536
    resolved: bool = False


def init_wires(lines: Iterator[str]) -> dict[str, Wire]:
    re_input_dest = r"(?P<input>.+) -> (?P<dest>[a-z]+)"
    wires: dict[str, Wire] = {}
    for line in lines:
        m = re.search(re_input_dest, line)
        if m is None:
            print(f"Incorrect input {line}")
            continue
        dest = m["dest"]
        if dest not in wires:
            wires[dest] = Wire(name=dest, input=m["input"])
    return wires


def solve_kit(wires: dict[str, Wire]) -> None:
    re_not = r"NOT ((:?P<value>\d+)|(?P<wire>[a-z]+))"
    re_binary_op = r"(?:(?P<value1>\d+)|(?P<wire1>[a-z]+)) (?P<op>AND|LSHIFT|OR|RSHIFT) (?:(?P<value2>\d+)|(?P<wire2>[a-z]+))"
    previous_unresolved = 0
    c_iterations = 0
    while(True):
        c_iterations += 1
        unresolved = 0
        for name, wire in wires.items():
            if wire.resolved:
                continue
            # signal -> wire
            try:
                value = int(wire.input)
                wire.value = value
                wire.resolved = True
                if name == "a":
                    print(f"Wire {name} resolved: {wire.value}")
                continue
            except ValueError:
                pass
            if wire.input in wires:
                wire1 = wires[wire.input]
                if wire1.resolved:
                    wire.value = wire1.value
                    wire.resolved = True
                    if name == "a":
                        print(f"Wire {name} resolved: {wire.value}")
                    continue
                unresolved += 1
                continue
            # NOT <value | wire>
            m = re.search(re_not, wire.input)
            if m is not None:
                not_value = None
                if "value" in m.groupdict():
                    not_value = int(m.groupdict()["value"])
                elif "wire" in m.groupdict():
                    not_wire = wires[m.groupdict()["wire"]]
                    if not_wire.resolved:
                        not_value = not_wire.value
                else:
                    raise ValueError(f"NOT expression incorrect for {name}: {wire.input}")
                if not_value is not None:
                    wire.value = not_value ^ 65535
                    wire.resolved = True
                    if name == "a":
                        print(f"Wire {name} resolved: {wire.value}")
                    continue
                unresolved += 1
                continue
            # binary op
            m = re.search(re_binary_op, wire.input)
            if m is not None:
                value1 = None
                if m.groupdict()["value1"] is not None:
                    value1 = int(m.groupdict()["value1"])
                elif m.groupdict()["wire1"] is not None:
                    wire1 = wires[m.groupdict()["wire1"]]
                    if wire1.resolved:
                        value1 = wire1.value
                else:
                    raise ValueError(f"Left side not recognized for {name}: {wire.input}")
                value2 = None
                if m.groupdict()["value2"] is not None:
                    value2 = int(m.groupdict()["value2"])
                elif m.groupdict()["wire2"] is not None:
                    wire2 = wires[m.groupdict()["wire2"]]
                    if wire2.resolved:
                        value2 = wire2.value
                else:
                    raise ValueError(f"Right side not recognize for {name}: {wire.input}")
                if (value1 is not None) and (value2 is not None):
                    match m.groupdict()["op"]:
                        case "AND":
                            binary_value = value1 & value2
                        case "OR":
                            binary_value = value1 | value2
                        case "LSHIFT":
                            binary_value = value1 << value2
                        case "RSHIFT":
                            binary_value = value1 >> value2
                        case _:
                            raise ValueError(f"Operand not recognized for {name}: {wire.input}")
                    wire.value = binary_value
                    wire.resolved = True
                    if name == "a":
                        print(f"Wire {name} resolved: {wire.value}")
                    continue
            else:
                print(f"Unrecognized input for {name}: {wire.input}")
            unresolved += 1
        if unresolved == 0:
            print("Yay! Everything is solved")
            break
        if unresolved == previous_unresolved:
            print("Nothing solved this iteration")
            break
        previous_unresolved = unresolved
        print(f"{unresolved} wires left")
        if c_iterations > len(wires):
            print(f"Too many iterations ({c_iterations}), number of wires is {len(wires)}")


def part1(lines: Iterator[str]) -> None:
    wires = init_wires(lines)
    solve_kit(wires)

    result = wires.get("a", None)
    print(f"Answer for 7.1 is {result}")


def part2(lines: Iterator[str]) -> None:
    wires = init_wires(lines)
    wires["b"].input = "956"
    solve_kit(wires)

    result = wires.get("a", None)
    print(f"Answer for 7.2 is {result}")
