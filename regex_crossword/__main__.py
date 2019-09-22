import sys
from pathlib import Path

from .crossword import Crossword


def main() -> None:
    packs_path = Path(sys.argv[1])
    cw = Crossword(packs_path)
    try:
        cw.mainloop()
    except KeyboardInterrupt:
        print('Thank you for playing!')


if __name__ == '__main__':
    main()
