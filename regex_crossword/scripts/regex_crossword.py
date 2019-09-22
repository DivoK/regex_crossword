import argparse
import os
from pathlib import Path

from ..crossword import Crossword

try:
    from .crawler import crawl
except ImportError:
    crawl = None

DEFAULT_LEVEL_PACKS_PATH = Path('level_packs')

SUCCESS = 0
FAILURE = -1


def parse_args() -> argparse.Namespace:
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
    crawler_group = parser.add_argument_group(
        'Crawler arguments', 'Arguments given to the crawler'
    )
    crawler_group.add_argument(
        '--crawl',
        default=False,
        action='store_true',
        help='Activate the crawler function (will override game functionality)',
    )
    crawler_group.add_argument(
        '--output',
        type=Path,
        default=DEFAULT_LEVEL_PACKS_PATH,
        help='Where to output the crawler data',
    )
    return parser.parse_args()


def game_main(level_packs_path: Path) -> None:
    cw = Crossword(level_packs_path)
    try:
        cw.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        print('Thank you for playing!')


def cli() -> int:
    args = parse_args()
    if args.crawl:
        if crawl is None:
            print(
                'Crawler isn\'t available.\nTry to reinstall the package using the extra requirement `[crawler]`.'
            )
            return FAILURE
        crawl(args.output)
        return SUCCESS
    level_packs: Path = (
        args.level_packs
        if args.level_packs
        else Path(os.environ.get('REGEXCW_LEVEL_PACKS', DEFAULT_LEVEL_PACKS_PATH))
    )
    if not level_packs.exists():
        print(f'Directory {level_packs} doesn\'t exist.')
        print('If you don\'t have any level packs, consider using the `--crawl` flag.')
        return FAILURE
    game_main(level_packs)
    return SUCCESS
