import curses
import _curses
from dataclasses import dataclass
from enum import IntEnum
import logging
import math
import os
from typing import Callable, Iterator, Optional


screen: Optional[curses.window] = None


class TCurses:
    """ curses helper """
#
    @classmethod
    def init(cls) -> None:
        # colour for background
        curses.init_pair(255, curses.COLOR_WHITE, 0xE8)
        cls.CP_BACKGROUND = curses.color_pair(255)
        # default text colour
        curses.init_pair(2, 0xDF, 0xE8)
        cls.CP_NORMAL = curses.color_pair(2)

        # cls.previous_curs_set = curses.curs_set(0)


class TOutputWindow:
    """ A window to display text """
    def __init__(self, cw_frame: curses.window, title: str) -> None:
        # Initialize the frame
        self._cw_frame = cw_frame
        self._title = title
        self._cw_frame.border()
        self._cw_frame.addstr(0, 3, f" {self._title} ")
        self._cw_frame.refresh()

        # Initialize the window for the contents
        begin_y, begin_x = self._cw_frame.getbegyx()
        max_y, max_x = self._cw_frame.getmaxyx()
        self._cw_contents = self._cw_frame.subwin(max_y - 2, max_x - 2, begin_y + 1, begin_x + 1)
        self._cw_contents.bkgd(TCurses.CP_BACKGROUND)
        self._cw_contents.scrollok(True)
        self._cw_contents.refresh()
        self.wrap: bool = True
        self._current_line: int = 0

    def add_message(self, message: str) -> None:
        """ Add a message, scroll if necessary """
        nlines, ncols = self._cw_contents.getmaxyx()
        def add_message_impl(message: str) -> None:
            assert(len(message) <= ncols)
            if self._current_line == nlines:
                self._cw_contents.scroll(1)
                self._current_line -= 1
            try:
                self._cw_contents.addstr(self._current_line, 0, message)
            except _curses.error:
                pass
            self._current_line += 1
        msg = message
        if len(message) > ncols:
            if self.wrap:
                for pos in range(0, len(message), ncols):
                    msg = message[pos:pos + ncols]
                    add_message_impl(msg)
                self._cw_contents.refresh()
                return
            else:
                msg = message[:ncols]
        add_message_impl(msg)
        self._cw_contents.refresh()


class TCursesHandler(logging.Handler):
    """ A handler for the logging system to add messages to the output
    window.
    """
    def __init__(self, w: TOutputWindow) -> None:
        logging.Handler.__init__(self)
        self._window: TOutputWindow = w

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record).rstrip(os.linesep)
            window = self._window
            window.add_message(message)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class Point:
    def __init__(self, y: int, x: int) -> None:
        self._y = y
        self._x = x

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.y == other.y) and (self.x == other.x)
        return False

    def __hash__(self):
        return self._y * 1000 + self._x


class Direction(IntEnum):
    Unknown = -1
    Right = 0
    Down = 1
    Left = 2
    Up = 3

    def toch(self) -> str:
        match self.value:
            case -1:
                return "\u2300"
            case 0:
                return ">"  # "\u2192"
            case 1:
                return "v"  # "\u2193"
            case 2:
                return "<"  # "\u2190"
            case 3:
                return "^"  # "\u2191"


@dataclass
class Score:
    c_turns: int = 0
    c_steps: float = float("inf")

    @property
    def score(self) -> int:
        if math.isinf(self.c_steps):
            return 10 ** 99
        return self.c_turns * 1000 + int(self.c_steps)

    def __lt__(self, other):
        return self.score < other.score


class Node:
    delta: list[tuple[int, int]] = [ (0, +1), (+1, 0), (0, -1), (-1, 0) ]
    def __init__(self,
                 y: int, x: int, 
                 value: str,
                 direction: Direction = Direction.Unknown, 
                 score: Score = Score()
    )-> None:
        """
        The score is a tuple of number of turns and number of steps.
        """
        self.y = y; self.x = x
        self.value = value
        self.direction = direction
        self.score = score
        self.parents: list["Node"] = []

    def follow(self) -> Iterator[tuple[int, int, Direction, Score]]:
        assert(
                (self.direction != Direction.Unknown) and
                (self.score.c_steps < float("inf"))
        )
        # continue in the same direction
        dy, dx = Node.delta[int(self.direction)]
        yield (
                self.y + dy, self.x + dx, 
                self.direction, 
                Score(self.score.c_turns, self.score.c_steps + 1)
        )
        # turn clockwise
        i: int = (int(self.direction) + 1 + 4) % 4
        dy, dx = Node.delta[i]
        yield (
                self.y + dy, self.x + dx, 
                Direction(i), 
                Score(self.score.c_turns + 1, self.score.c_steps + 1)
        )
        # turn counterclockwise
        i = (int(self.direction) - 1 + 4) % 4
        dy, dx = Node.delta[i]
        yield (
                self.y + dy, self.x + dx, 
                Direction(i), 
                Score(self.score.c_turns + 1, self.score.c_steps + 1)
        )

    def __lt__(self, other: "Node") -> bool:
        """ Comparison method, used for the Djikstra priority queue """
        # return self.score.c_steps < other.score.c_steps
        return self.score < other.score


class Maze:
    def __init__(self, lines: Iterator[str]):
        self._maze: list[list[Node]] = []
        for y, line in enumerate(lines):
            row: list[Node] = []
            for x, cell in enumerate(line):
                match cell:
                    case "S":
                        self._start = Point(y, x)
                        cell = "."
                    case "E":
                        self._end = Point(y, x)
                        cell = "."
                    case "#" | ".":
                        pass
                    case _:
                        continue
                node = Node(y, x, cell)
                row.append(node)
            self._maze.append(row)
        node_start = self._maze[self._start.y][self.start.x]
        node_start.direction = Direction.Right
        node_start.score.c_steps = 0

        self.onchange: Optional[Callable[[Node], None]] = None

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end

    @property
    def height(self) -> int:
        return len(self._maze)

    @property
    def width(self) -> int:
        return len(self._maze[0])

    @property
    def rows(self) -> Iterator[list[Node]]:
        yield from self._maze

    def djikstra(self) -> int:
        heap: list[Node] = []
        # initialize directions, scores, and parents
        for y, row in enumerate(self._maze):
            for x, node in enumerate(row):
                if node.value == "#": continue
                if (y == self._start.y) and (x == self.start.x):
                    node.direction = Direction.Right
                    node.score = Score(0, 0)
                else:
                    node.direction = Direction.Unknown
                    node.score = Score()
                node.parents = []
                # heapq.heappush(heap, node)
                heap.append(node)

        while len(heap) > 0:
            index: int = 0
            score: Score = heap[index].score
            for i in range(0, len(heap)):
                if heap[i].score < score:
                    index = i
                    score = heap[i].score
            u: Node = heap.pop(index)
            for y, x, d, s in u.follow():
                v: Node = self._maze[y][x]
                if v.value == "#": continue
                if s < v.score:
                    v.direction = d
                    v.score = s
                    v.parents.append(u)
                    logging.info(f"u({u.y},{u.x}),{u.direction.name},({u.score.c_turns},{u.score.c_steps})->v({v.y},{v.x}),{v.direction.name},({v.score.c_turns},{v.score.c_steps})")
                    self._onchange(v)

        result = self._maze[self._end.y][self._end.x].score.score
        logging.info(f"Found score of {result}")
        return result

    def _onchange(self, node: Node) -> None:
        if self.onchange:
            self.onchange(node)


class TMazeWindow:
    def __init__(self, maze: Maze, cw_frame: curses.window) -> None:
        self._maze = maze
        self._maze.onchange = self.maze_changed
        self._cw_frame = cw_frame
        self._cp_contents = curses.newpad(maze.height, maze.width + 1)
        self._cp_contents.bkgd(TCurses.CP_BACKGROUND)
        self._cp_contents.attrset(TCurses.CP_NORMAL)
        for y, row in enumerate(self._maze.rows):
            for x, node in enumerate(row):
                self._cp_contents.addch(y, x, node.value)
        self._cp_contents.addch(self._maze.start.y, self._maze.start.x, "S")
        self._cp_contents.addch(self._maze._end.y, self._maze._end.x, "E")
        self._current_column = self._current_line = 0

    def refresh(self) -> None:
        begin_y, begin_x = self._cw_frame.getbegyx()
        max_y, max_x = self._cw_frame.getmaxyx()
        self._cp_contents.refresh(
                self._current_column, self._current_line,
                begin_y + 1, begin_x + 1,
                max_y - 2, max_x - 2
        )

    def maze_changed(self, node: Node) -> None:
        self._cp_contents.addch(node.y, node.x, node.direction.toch())
        self.refresh()


def part1_curses(cw_main: curses.window, lines: Iterator[str]) -> int:
    global screen
    screen = cw_main

    TCurses.init()
    cw_main.bkgd(TCurses.CP_BACKGROUND)
    cw_main.refresh()

    maze = Maze(lines)
    score = -1
    cw_messages = curses.newwin(7, curses.COLS, curses.LINES - 10, 0)
    cw_messages.bkgd(TCurses.CP_BACKGROUND)
    cw_messages.attrset(TCurses.CP_NORMAL)
    logging.root.addHandler(TCursesHandler(TOutputWindow(cw_messages, "Output")))
    logging.root.setLevel(logging.DEBUG)

    cw_maze_frame = curses.newwin(curses.LINES - 10, curses.COLS - 25, 0, 0)
    cw_maze_frame.bkgd(TCurses.CP_BACKGROUND)
    cw_maze_frame.attrset(TCurses.CP_NORMAL)
    cw_maze_frame.border()
    cw_maze_frame.addstr(0, 3, " Maze ")
    cw_maze_frame.refresh()
    wnd_maze = TMazeWindow(maze, cw_maze_frame)
    wnd_maze.refresh()

    cw_details = curses.newwin(curses.LINES - 10, 25, 0, curses.COLS - 25)
    cw_details.bkgd(TCurses.CP_BACKGROUND)
    cw_details.attrset(TCurses.CP_NORMAL)
    cw_details.border()
    cw_details.addstr(0, 3, " Details ")
    cw_details.refresh()
    score = maze.djikstra()
    cw_main.getch()
    return score


def part1(lines: Iterator[str]) -> None:
    score = curses.wrapper(part1_curses, lines)
    print(f"Answer for 16.1 is {score}")
