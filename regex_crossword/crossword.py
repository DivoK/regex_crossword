import curses
import curses.ascii
import string
from pathlib import Path

from .game import Game
from .level_pack import LevelPack
from .utils import Coordinate, popup_message

INTRO = '''Welcome to the Regex Crossword!

You can interact with any text on this screen by pressing the coresponding {KEY}.
If you need any help, please press {?}.

Choose your level pack:
'''  # The first text on the selection screen.

HELP_TEXT = '''Hello and welcome to the Regex Crossword!

The game goes like this:
You will be presented with a grid for you to fill with characters.
There will also be definitions telling you how to fill the grid. Just like an ordinary crossword!
The twist? Each "definition" is actually a Regular Expression that will try to match against the respectful row or column.
Your goal? Fill the entire grid so that every regex will match its coresponding string!

KEYS:
Navigate the grid using the {ARROW KEYS}. When you think you're done, press {ENTER} to validate yourself!
If your input was valid, you will move on to the next level in the level pack.
Also, you can navigate back and forth between levels in your chosen level pack by pressing {PAGE_DOWN} and {PAGE_UP} respectfully.
You can go back from any screen (including this help or the main selection) by pressing {ESCAPE}.

On another note, all regexes are computed in real time when you try to validate your input.
There is no predefined answer so if you fail to validate a level be sure to check the regexes again!

Happy regexing!
'''  # The help text, explaining the game and keys to the player.


class Crossword:
    """
    Class unifying all the logic needed to fully play the game, from loading the levels to playing them.
    """

    def __init__(self, level_packs_path: Path):
        self.pack_id_pairs = {
            pack_id: Path(pack_path)
            for pack_id, pack_path in zip(
                string.digits + string.ascii_letters, sorted(level_packs_path.iterdir())
            )
        }  # Dict mapping between an arbitrary id (to allow easy selection for the user) an the actual pack path.
        self.selection_screen_str = INTRO + '\n'.join(
            f'{{{i}}} {path.stem}' for i, path in self.pack_id_pairs.items()
        )  # The entire selection screen as a concatenated string.
        self.help_str = HELP_TEXT  # The entire help text as a concatenated string.
        self.stdscr = None

    def _display_help(self) -> None:
        """
        Pop up the help message to the screen.

        :return: none.
        :rtype: None
        """
        help_offset_y = int(curses.LINES * (1 / 5))
        help_offset_x = int(curses.COLS * (1 / 7))
        help_position = Coordinate(help_offset_y, help_offset_x)
        exit_keys = [curses.ascii.ESC]
        popup_message(self.help_str, help_position, exit_keys)

    def _handle_input(self, char: int) -> None:
        """
        Handle the given character input:
        - If it's a valid pack id character, initialize that pack and play each level.
        - If it's the special character '?', display the help message.

        :param char: the character (int value) to handle.
        :type char: int
        :return: none.
        :rtype: None
        """
        if chr(char) in self.pack_id_pairs:
            pack = LevelPack(self.pack_id_pairs[chr(char)])
            i = 0
            while 0 <= i < len(pack):
                self.stdscr.clear()
                self.stdscr.refresh()
                g = Game(pack[i])
                ret_val = g.play_level()
                if ret_val == 0:
                    break
                i += ret_val
        elif chr(char) == '?':
            self._display_help()

    def mainloop(self) -> None:
        """
        Start a curses instance, display the main selection screen and handle each input until ESCAPE is pressed.

        :return: none.
        :rtype: None
        """

        def _mainloop(stdscr) -> None:
            self.stdscr = stdscr
            self.stdscr.addstr(self.selection_screen_str)
            self.stdscr.refresh()
            curses.curs_set(0)
            char = self.stdscr.getch()
            while char != curses.ascii.ESC:
                curses.curs_set(1)
                self._handle_input(char)
                self.stdscr.clear()
                self.stdscr.addstr(self.selection_screen_str)
                self.stdscr.refresh()
                curses.curs_set(0)
                char = self.stdscr.getch()

        curses.wrapper(_mainloop)
