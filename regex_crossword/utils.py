import curses
import dataclasses
import typing


@dataclasses.dataclass
class Coordinate:
    row: int
    col: int


def popup_message(message: str, position: Coordinate, exit_keys: typing.Iterable) -> None:
    prev_cursor = curses.curs_set(0)
    message_split = message.splitlines()
    message_width = len(max(message_split, key=len))
    message_length = len(message_split)
    message_box = curses.newwin(
        message_length + 2, message_width + 3, position.row - 1, position.col - 1
    )
    message_box.border()
    message_box.refresh()
    window_message = curses.newwin(
        message_length, message_width + 1, position.row, position.col
    )
    window_message.addstr(message.strip())
    window_message.refresh()
    char = window_message.getch()
    while char not in exit_keys:
        char = window_message.getch()
    curses.curs_set(prev_cursor)
