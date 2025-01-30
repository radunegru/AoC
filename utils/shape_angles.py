"""
Utility for part 2 day 12 2024.
Maintains a list of shapes and the corresponding angles. This list is used to
compute the number of sides for a plot (the number of sides in a polygon equals
the number of angles).
"""
import os


from shape import Shape


ALL_SHAPES:dict[int, Shape] = {}


class _Getch:
    """
    Gets a single character from standard input. Dos not echo to the screen.
    https://code.activestate.com/recipes/134892/
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()


# class Shape:
#     def __init__(self, shape_id: int, *, form: str = ""):
#         self._shape_id: int = shape_id
#         self._form: str = form

#         self._ref_shape: int = -1
#         self._similar_shapes: set[int] = set()

#         self._shape_str: str = ""
#         self._angles: int = -1

#     def __hash__(self):
#         return self._shape_id

#     @property
#     def shape_id(self) -> int:
#         return self._shape_id

#     @property
#     def form(self) -> str:
#         return self._form
#     @form.setter
#     def form(self, value: str) -> None:
#         self._form = value

#     @property
#     def ref_shape(self) -> int:
#         return self._ref_shape
#     @ref_shape.setter
#     def ref_shape(self, value: int) -> None:
#         self._ref_shape = value

#     @property
#     def similar_shapes(self) -> set[int]:
#         return self._similar_shapes

#     @property
#     def shape_str(self) -> str:
#         """
#         Returns a compressed string representation of the shape.
#         A "." (dot) represents a plot in a different region as the current plot.
#         A "\u2588" (full block) represents a plot in the same region as the
#         current plot.
#         The current plot is always in the middle.
#         """
#         if self._shape_str == "":
#             self._shape_str = \
#                 f"{((self.shape_id & 240) << 1) + (1 << 4) + (self.shape_id & 15):09b}" \
#                 .replace("1", "\u2588") \
#                 .replace("0", ".")
#         return self._shape_str

#     @property
#     def angles(self) -> int:
#         """
#         Returns the number of angles on the shape.
#         The number of angles is -1 if the shape is not initialized.
#         """
#         return self._angles
#     @angles.setter
#     def angles(self, value: int) -> None:
#         if 0 <= value <= 4:
#             self._angles = value
#         else:
#             raise ValueError(f"A shape may have between 0 and 4 angles. {value} is invalid")

#     def rotate(self) -> "Shape":
#         """
#         Returns a new shape by rotating the current shape clockwise.
#         """
#         rotated_shape_id = \
#             ((self.shape_id & 0b00000001) << 2) | \
#             ((self.shape_id & 0b00000010) << 3) | \
#             ((self.shape_id & 0b00000100) << 5) | \
#             ((self.shape_id & 0b00001000) >> 2) | \
#             ((self.shape_id & 0b00010000) << 2) | \
#             ((self.shape_id & 0b00100000) >> 5) | \
#             ((self.shape_id & 0b01000000) >> 3) | \
#             ((self.shape_id & 0b10000000) >> 2)
#         return Shape(rotated_shape_id, form=self.form + "\u21BB")

#     def flip_vert(self) -> "Shape":
#         """
#         Returns a new shape by vertically flipping the current shape.
#         """
#         flipped_shape_id = \
#             ((self.shape_id & 0b00100001) << 2) | \
#             ((self.shape_id & 0b01000010)     ) | \
#             ((self.shape_id & 0b10000100) >> 2) | \
#             ((self.shape_id & 0b00001000) << 1) | \
#             ((self.shape_id & 0b00010000) >> 1)
#         return Shape(flipped_shape_id, form=self.form + "flipv")

#     def flip_horz(self) -> "Shape":
#         """
#         Returns a new shape by horizontally flipping the current shape.
#         """
#         flipped_shape_id = \
#             ((self.shape_id & 0b00000111) << 5) | \
#             ((self.shape_id & 0b00011000)     ) | \
#             ((self.shape_id & 0b11100000) >> 5)
#         return Shape(flipped_shape_id, form=self.form + "fliph")

#     def pretty_print(self) -> None:
#         print(f"{self.shape_id:3} {self.shape_str} {self.shape_str[0:3]}")
#         print(f"{self.form:13} {self.shape_str[3:6]}")
#         print(f"{" ":13} {self.shape_str[6:9]}")

#     def changes(self) -> Iterator["Shape"]:
#         """
#         Returns an iterator with every possible change of the current shape.
        
#         The shapes returned by changes have the same number of angles.
#         """
#         base_shapes: list[Shape] = [ self ]

#         change: "Shape" = self.flip_vert()
#         base_shapes.append(change)
#         yield change

#         change = self.flip_horz()
#         base_shapes.append(change)
#         yield change

#         yields: set[int] = { shape.shape_id for shape in base_shapes }
#         for shape in base_shapes:
#             for _ in range(3):
#                 shape = shape.rotate()
#                 if shape.shape_id not in yields:
#                     yield shape
#                     yields.add(shape.shape_id)

#     def _to_dict(self) -> dict[str, str]:
#         return {
#             "shape_id": str(self._shape_id),
#             "form": self._form,
#             "ref_shape": str(self._ref_shape),
#             "similar_shapes": str(self._similar_shapes),
#             "angles": str(self._angles)
#         }

#     @classmethod
#     def _from_dict(cls, shape_dict) -> "Shape":
#         result = Shape(int(shape_dict["shape_id"]), form=shape_dict["form"])
#         result._ref_shape = int(shape_dict["ref_shape"])
#         result._similar_shapes = ast.literal_eval(shape_dict["similar_shapes"])
#         result._angles = int(shape_dict["angles"])
#         return result

#     @staticmethod
#     def generate_all_shapes() -> dict[int, "Shape"]:
#         all_shapes: dict[int, Shape] = {}
#         for shape_id in range(256):
#             similar_shapes: set[int] = { shape_id }
#             shape = Shape(shape_id)
#             for change in shape.changes():
#                 if change.shape_id in all_shapes:
#                     shape.ref_shape = all_shapes[change.shape_id].ref_shape
#                     break
#                 similar_shapes.add(change.shape_id)
#             else:
#                 shape.similar_shapes.clear()
#                 shape.similar_shapes.update(similar_shapes)
#                 shape.ref_shape = shape_id # set ref to self
#             all_shapes[shape_id] = shape
#         return all_shapes

#     @staticmethod
#     def serialize_all_shapes(all_shapes: dict[int, "Shape"], fp: TextIO) -> None:
#         fp.write(str({ shape_id: shape._to_dict() for shape_id, shape in all_shapes.items() }))

#     @staticmethod
#     def deserialize_all_shapes(fp: TextIO) -> dict[int, "Shape"]:
#         s: str = fp.read()
#         result = { shape_id: Shape._from_dict(d)
#                   for shape_id, d in ast.literal_eval(s).items() }
#         return result


# def init_shapes() -> None:
#     """
#     This method initializes shapes:
#     - asks the user to start fresh or read from file
#     - if there are unitialized reference shapes:
#       - asks the user to fill the angles for the unitialized shapes
#       - ask the user where to save the shapes
#     - available commands:
#       - save file
#       - review all reference shapes
#       - review all non reference shapes
#       - review specific shape
#     """
#     all_shapes: dict[int, Shape] = {}

#     def save_all_shapes() -> None:
#         while True:
#             answer = input("Give a file name to save (shapes.json) q(uit): ").lower()
#             if answer in [ "q", "quit" ]:
#                 break
#             if answer == "":
#                 answer = "shapes.json"
#             try:
#                 with open(answer, "w") as fp:
#                     Shape.serialize_all_shapes(all_shapes, fp)
#                 break
#             except Exception as ex:
#                 print(ex)

#     def review_shapes() -> None:
#         while True:
#             answer = input("Id of shape to review or q(uit): ").lower()
#             if answer in [ "q", "quit" ]:
#                 break
#             try:
#                 shape = all_shapes[int(answer)]
#                 if shape.shape_id != shape.ref_shape:
#                     print(f"/!\\ Not a reference shape ({shape.ref_shape})")
#                 while True:
#                     answer = input("How many angles for this shape? 0..4 q(uit) ").lower()
#                     if answer in [ "q", "quit" ]:
#                         break
#                     try:
#                         angles: int = int(answer)
#                         shape.angles = angles
#                         break
#                     except Exception as ex:
#                         print(ex)
#             except Exception as ex:
#                 print(ex)


#     answer = ""
#     while answer not in [ "y", "n", "yes", "no" ]:
#         answer = input("Do you want to start fresh? Y[es]/N[o] ").lower()

#     if answer in [ "y", "yes" ]:
#         all_shapes = Shape.generate_all_shapes()
#         b_continue = True
#         for shape in all_shapes.values():
#             if shape.shape_id == shape.ref_shape:
#                 shape.pretty_print()
#                 while True:
#                     answer = input("How many angles for this shape? 0..4, q(uit), s(kip) ").lower()
#                     if answer in [ "q", "quit" ]:
#                         b_continue = False
#                         break
#                     elif answer in [ "s", "skip" ]:
#                         break
#                     try:
#                         angles: int = int(answer)
#                         shape.angles = angles
#                         for similar_id in shape.similar_shapes:
#                             all_shapes[similar_id].angles = angles
#                         break
#                     except Exception as ex:
#                         print(ex)
#             if not b_continue:
#                 break

#         save_all_shapes()
#     else:
#         while True:
#             answer = input("Give a file name to load (shapes.json) q(uit): ").lower()
#             if answer in [ "q", "quit" ]:
#                 break
#             if answer == "":
#                 answer = "shapes.json"
#             try:
#                 with open(answer, "r") as fp:
#                     all_shapes = Shape.deserialize_all_shapes(fp)
#                 break
#             except Exception as ex:
#                 print(ex)
#     while True:
#         answer = input("S(ave) | R(eview) | V(iew) shape_id | Q(uit) ").lower()
#         match answer:
#             case "q":
#                 return
#             case "s":
#                 save_all_shapes()
#             case "r":
#                 review_shapes()
#             case _:
#                 if len(answer.split()) == 2:
#                     v, s= answer.split()
#                     try:
#                         shape = all_shapes[int(s)]
#                         shape.pretty_print()
#                         print(f"angles={shape.angles}, ref={shape.ref_shape}, similar={shape.similar_shapes}")
#                     except:
#                         continue


def get_shape_from_command(words: list[str]) -> Shape:
    global ALL_SHAPES

    if len(ALL_SHAPES) == 0:
        raise ValueError("Unitialized: please use new of load")
    if len(words) < 2:
        raise ValueError("Please specify shape id")
    try:
        return ALL_SHAPES[int(words[1])]
    except ValueError:
        raise ValueError("Shape id must be an integer")
    except KeyError:
        raise ValueError(f"Shape id must be an integer between 0 and {len(ALL_SHAPES)}")


def load_shapes(words: list[str]) -> None:
    global ALL_SHAPES

    filename:str = words[1] if len(words) > 1 else "shapes.json"
    try:
        with open(filename, "r") as fp:
            ALL_SHAPES = Shape.deserialize_all_shapes(fp)
        print(f"Loaded {filename}, {len(ALL_SHAPES)} shaped found")
    except Exception as ex:
        print(f"Error loading {filename}: {ex}")


def write_shapes(words: list[str]) -> None:
    global ALL_SHAPES

    filename:str = words[1] if len(words) > 1 else "shapes.json"
    try:
        with open(filename, "w") as fp:
            Shape.serialize_all_shapes(ALL_SHAPES, fp)
        print(f"Wrote {filename}")
    except Exception as ex:
        print(f"Error writing {filename}: {ex}")


def display_status() -> None:
    global ALL_SHAPES

    print(f"Total number of shapes: {len(ALL_SHAPES)}")
    c_ref: int = 0
    c_similar: int = 0
    c_ref_initialized: int = 0
    wrong_similar: list[int] = []
    for shape in ALL_SHAPES.values():
        if shape.shape_id == shape.ref_shape:
            c_ref += 1
            c_ref_initialized += 1 if shape.angles != -1 else 0
        else:
            c_similar += 1
            if shape.angles != ALL_SHAPES[shape.ref_shape].angles:
                wrong_similar.append(shape.shape_id)
    print(f"Number of reference shapes: {c_ref}")
    print(f"Number of similar shapes: {c_similar} ({len(ALL_SHAPES) - c_ref})")
    print(f"Number of initialized reference shapes: {c_ref_initialized}")
    if len(wrong_similar) != 0:
        print(f"Wrong similar shapes: {wrong_similar}")


def _display_shape(shape: Shape) -> None:
    shape.pretty_print()
    print(f"Reference shape = {shape.ref_shape}")
    print(f"Similar shapes: {shape.similar_shapes}")


def display_shape(words: list[str]) -> None:
    try:
        _display_shape(get_shape_from_command(words))
    except Exception as ex:
        print(ex)


def edit_shape(words: list[str]) -> None:
    global ALL_SHAPES

    try:
        shape = get_shape_from_command(words)
        if shape.shape_id != shape.ref_shape:
            print(f"/!\\ Not a reference shape ({shape.ref_shape})")
        shape.pretty_print()
        if shape.angles != -1:
            print(f"Currently there are {shape.angles} angles for this shape")
        answer = input("How many angles for this shape? 0..4 q(uit) ").lower()
        if answer in [ "q", "quit" ]: return
        angles = int(answer)
        shape.angles = int(answer)
        for similar_shape_id in shape.similar_shapes:
            ALL_SHAPES[similar_shape_id].angles = angles
            print(f"Updated similar shape {similar_shape_id}")
        print()
        _display_shape(shape)
    except Exception as ex:
        print(ex)


def display_reference_shapes() -> None:
    global ALL_SHAPES

    _, lines = os.get_terminal_size()
    # 6 lines per shape
    # lines // 6 shapes per page
    page_size = lines // 6 # magic 6 is the number of lines for a shape
    answer = " " # display a page
    ref_shapes = [ shape for shape in ALL_SHAPES.values() if shape.shape_id == shape.ref_shape ]
    iterator = iter(ref_shapes)
    while True:
        try:
            match answer:
                case " ":
                    for _ in range(page_size):
                        shape = next(iterator)
                        _display_shape(shape)
                        print()
                case "j":
                    shape = next(iterator)
                    _display_shape(shape)
                    print()
                case "q":
                    break
        except StopIteration:
            pass
        answer = getch()


def display_help() -> None:
    print(
"""Rudimentary shape management
l(oad) [<filename>] - read shapes from file (shapes.json by default)
w(rite) [<filename>] - write shapes to file (shapes.json by default)
s(tatus) - display statistics
v(iew) <shape id> - display information about specified shape
e(dit) shape - modify the specified shape
dr - display reference shapes
h(elp) - display this screen
q(uit) - quit application
""")


def take2() -> None:
    """
    Take two for the application to maintain shapes' angles.
    - start fresh - new
    - display all references - display
    - display all shapes without angles - unitialized
    - edit a shape - edit <shape_id>
    - edit all unitialized references - complete
    """
    while True:
        words:list[str] = input("shape > ").split()
        command = words[0].lower()
        match command:
            case "l" | "load":
                load_shapes(words)
            case "w" | "write":
                write_shapes(words)
            case "s" | "status":
                display_status()
            case "v" | "view":
                display_shape(words)
            case "e" | "edit":
                edit_shape(words)
            case "dr":
                display_reference_shapes()
            case "h" | "help":
                display_help()
            case "q" | "quit":
                break
            case _:
                print(f"{command} not implemented yet")


if __name__ == "__main__":
    # init_shapes()
    take2()
# 14, 50, 51, 
