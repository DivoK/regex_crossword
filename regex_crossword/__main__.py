import curses
import sys
from pathlib import Path

from .crossword import Crossword


def main(stdscr) -> None:
    packs_path = Path(sys.argv[1])
    cw = Crossword(packs_path)
    cw.mainloop(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)
