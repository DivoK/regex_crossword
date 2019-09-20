import curses
import sys
from pathlib import Path

from .game import Game
from .level_pack import LevelPack


def main(stdscr) -> None:
    pack_path = Path(sys.argv[1])
    pack = LevelPack(pack_path)
    for level in pack:
        g = Game(level)
        g.play_level()
        del g
        stdscr.clear()
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
