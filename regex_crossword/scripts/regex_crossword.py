import argparse
import os
from pathlib import Path

from ..crossword import Crossword

try:
    from .scraper import scrape
except ImportError:
    # This means the user haven't installed the `scraper` extra, which is fine.
    scrape = None

DEFAULT_LEVEL_PACKS_PATH = Path(
    'level_packs'
)  # Default path where level packs will be looked for.

SUCCESS = 0
FAILURE = -1


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments.

    :return: argparse paresd arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description='Start the game')
    game_group = parser.add_argument_group(
        'Game arguments', 'Arguments that affect the way the game is loaded and played'
    )
    game_group.add_argument(
        '--level-packs',
        metavar='PATH',
        type=Path,
        help='Path to a directory containing the level packs',
    )
    scraper_group = parser.add_argument_group(
        'scraper arguments', 'Arguments given to the scraper'
    )
    scraper_group.add_argument(
        '--scrape',
        default=False,
        action='store_true',
        help='Activate the scraper function (will override game functionality)',
    )
    scraper_group.add_argument(
        '--output',
        type=Path,
        default=DEFAULT_LEVEL_PACKS_PATH,
        help='Where to output the scraper data',
    )
    return parser.parse_args()


def game_main(level_packs_path: Path) -> None:
    """
    Create a new Crossword instance and start the game's mainloop.

    :param level_packs_path: path to a directory containing level packs.
    :type level_packs_path: Path
    :return: none.
    :rtype: None
    """
    cw = Crossword(level_packs_path)
    try:
        cw.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        print('Thank you for playing!')


def cli() -> int:
    """
    Main entry point for the CLI.

    :return: exit code.
    :rtype: int
    """
    args = parse_args()
    if args.scrape:
        if scrape is None:
            print(
                'Scraper isn\'t available.\nTry to reinstall the package using the extra requirement `[scraper]`.'
            )
            return FAILURE
        scrape(args.output)
        return SUCCESS
    level_packs: Path = (
        args.level_packs
        if args.level_packs
        else Path(os.environ.get('REGEXCW_LEVEL_PACKS', DEFAULT_LEVEL_PACKS_PATH))
    )
    if not level_packs.exists():
        print(f'Directory {level_packs} doesn\'t exist.')
        print('If you don\'t have any level packs, consider using the `--scrape` flag.')
        return FAILURE
    game_main(level_packs)
    return SUCCESS
