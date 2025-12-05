import ast
from typing import Iterator, TextIO


class Shape:
    def __init__(self, shape_id: int, *, form: str = ""):
        self._shape_id: int = shape_id
        self._form: str = form

        self._ref_shape: int = -1
        self._similar_shapes: set[int] = set()

        self._shape_str: str = ""
        self._angles: int = -1

    def __hash__(self):
        return self._shape_id

    @property
    def shape_id(self) -> int:
        return self._shape_id

    @property
    def form(self) -> str:
        return self._form
    @form.setter
    def form(self, value: str) -> None:
        self._form = value

    @property
    def ref_shape(self) -> int:
        return self._ref_shape
    @ref_shape.setter
    def ref_shape(self, value: int) -> None:
        self._ref_shape = value

    @property
    def similar_shapes(self) -> set[int]:
        return self._similar_shapes

    @property
    def shape_str(self) -> str:
        """
        Returns a compressed string representation of the shape.
        A "." (dot) represents a plot in a different region as the current plot.
        A "\u2588" (full block) represents a plot in the same region as the
        current plot.
        The current plot is always in the middle.
        """
        if self._shape_str == "":
            self._shape_str = \
                f"{((self.shape_id & 240) << 1) + (1 << 4) + (self.shape_id & 15):09b}" \
                .replace("1", "\u2588") \
                .replace("0", ".")
        return self._shape_str

    @property
    def angles(self) -> int:
        """
        Returns the number of angles on the shape.
        The number of angles is -1 if the shape is not initialized.
        """
        return self._angles
    @angles.setter
    def angles(self, value: int) -> None:
        if 0 <= value <= 4:
            self._angles = value
        else:
            raise ValueError(f"A shape may have between 0 and 4 angles. {value} is invalid")

    def rotate(self) -> "Shape":
        """
        Returns a new shape by rotating the current shape clockwise.
        """
        rotated_shape_id = \
            ((self.shape_id & 0b00000001) << 2) | \
            ((self.shape_id & 0b00000010) << 3) | \
            ((self.shape_id & 0b00000100) << 5) | \
            ((self.shape_id & 0b00001000) >> 2) | \
            ((self.shape_id & 0b00010000) << 2) | \
            ((self.shape_id & 0b00100000) >> 5) | \
            ((self.shape_id & 0b01000000) >> 3) | \
            ((self.shape_id & 0b10000000) >> 2)
        return Shape(rotated_shape_id, form=self.form + "\u21BB")

    def flip_vert(self) -> "Shape":
        """
        Returns a new shape by vertically flipping the current shape.
        """
        flipped_shape_id = \
            ((self.shape_id & 0b00100001) << 2) | \
            ((self.shape_id & 0b01000010)     ) | \
            ((self.shape_id & 0b10000100) >> 2) | \
            ((self.shape_id & 0b00001000) << 1) | \
            ((self.shape_id & 0b00010000) >> 1)
        return Shape(flipped_shape_id, form=self.form + "flipv")

    def flip_horz(self) -> "Shape":
        """
        Returns a new shape by horizontally flipping the current shape.
        """
        flipped_shape_id = \
            ((self.shape_id & 0b00000111) << 5) | \
            ((self.shape_id & 0b00011000)     ) | \
            ((self.shape_id & 0b11100000) >> 5)
        return Shape(flipped_shape_id, form=self.form + "fliph")

    def pretty_print(self) -> None:
        print(f"{self.shape_id:3} {self.shape_str} {self.shape_str[0:3]}")
        print(f"{self.form:13} {self.shape_str[3:6]}")
        print(f"\u2221{self.angles:<12} {self.shape_str[6:9]}")

    def changes(self) -> Iterator["Shape"]:
        """
        Returns an iterator with every possible change of the current shape.
        
        The shapes returned by changes have the same number of angles.
        """
        base_shapes: list[Shape] = [ self ]

        change: "Shape" = self.flip_vert()
        base_shapes.append(change)
        yield change

        change = self.flip_horz()
        base_shapes.append(change)
        yield change

        yields: set[int] = { shape.shape_id for shape in base_shapes }
        for shape in base_shapes:
            for _ in range(3):
                shape = shape.rotate()
                if shape.shape_id not in yields:
                    yield shape
                    yields.add(shape.shape_id)

    def _to_dict(self) -> dict[str, str]:
        return {
            "shape_id": str(self._shape_id),
            "form": self._form,
            "ref_shape": str(self._ref_shape),
            "similar_shapes": str(self._similar_shapes),
            "angles": str(self._angles)
        }

    @classmethod
    def _from_dict(cls, shape_dict: dict[str, str]) -> "Shape":
        result: "Shape" = Shape(int(shape_dict["shape_id"]), form=shape_dict["form"])
        result._ref_shape = int(shape_dict["ref_shape"])
        result._similar_shapes = ast.literal_eval(shape_dict["similar_shapes"])
        result._angles = int(shape_dict["angles"])
        return result

    @staticmethod
    def generate_all_shapes() -> dict[int, "Shape"]:
        all_shapes: dict[int, Shape] = {}
        for shape_id in range(256):
            similar_shapes: set[int] = { shape_id }
            shape = Shape(shape_id)
            for change in shape.changes():
                if change.shape_id in all_shapes:
                    shape.ref_shape = all_shapes[change.shape_id].ref_shape
                    break
                similar_shapes.add(change.shape_id)
            else:
                shape.similar_shapes.clear()
                shape.similar_shapes.update(similar_shapes)
                shape.ref_shape = shape_id # set ref to self
            all_shapes[shape_id] = shape
        return all_shapes

    @staticmethod
    def serialize_all_shapes(all_shapes: dict[int, "Shape"], fp: TextIO) -> None:
        fp.write(str({ shape_id: shape._to_dict() for shape_id, shape in all_shapes.items() }))

    @staticmethod
    def deserialize_all_shapes(fp: TextIO) -> dict[int, "Shape"]:
        s: str = fp.read()
        result: dict[int, "Shape"] = { shape_id: Shape._from_dict(d)
                  for shape_id, d in ast.literal_eval(s).items() }
        return result
