import curses
import string
from pathlib import Path

from .game import Game
from .level_pack import LevelPack

INTRO = """
Welcome to the Regex Crossword!
Choose your level pack:
"""


class Crossword:
    def __init__(self, level_packs_path: Path):
        self.pack_id_pairs = {
            pack_id: Path(pack_path)
            for pack_id, pack_path in zip(
                string.digits + string.ascii_letters, level_packs_path.iterdir()
            )
        }
        self.intro = INTRO + '\n'.join(
            f'{{{i}}} {path.stem}' for i, path in self.pack_id_pairs.items()
        )

    def handle_input(self, char: int) -> None:
        if char in self.pack_id_pairs:
            pack = LevelPack(self.pack_id_pairs[char])
            for level in pack:
                self.stdscr.clear()
                self.stdscr.refresh()
                g = Game(level)
                g.play_level()
                del g

    def mainloop(self, stdscr):
        self.stdscr = stdscr
        char = self.stdscr.getch()
        while char != curses.ascii.ESC:
            self.stdcr.addstr(self.intro)
            self.stdscr.refresh()
            self.handle_input(char)
            char = self.stdscr.getch()
