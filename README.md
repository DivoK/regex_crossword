# Regex Crossword

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/regex_crossword.svg)](https://pypi.python.org/pypi/regex_crossword/)
[![PyPI version fury.io](https://badge.fury.io/py/regex_crossword.svg)](https://pypi.python.org/pypi/regex_crossword/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Terminal Freaks rejoice!

Based on the [Regex Crossword](https://regexcrossword.com/), this is an implementation written in pure python using only the standard library to play the game offline entirely from your shell.

If you aren't familiar with the concpet of a regex crossword, it's a blank crossword grid that you need to fill so that each row and column will match the specified regex. It's a fun exercise to your regex abilities and an interactive way to learn about them  and practice while playing.

I'm a bit of a terminal freak myself and so the moment I started playing the wonderful online version it seemed so natural to me that there needs to be a version of the concept playable from the shell, so I made one using nothing but Python's `curses` module.

## Installation

Use the Python package manager [pip](https://pip.pypa.io/en/stable/) to install `regex_crossword`.

```bash
pip install regex_crossword
```

To install the scraper functionality as well (more on this below) use:

```bash
pip install regex_crossword[scraper]
```

> Note: the scraper uses the Selenium 3rd party package that might need extra setup to be used (specifically the Chrome WebDriver). If you encounter any problems I advise you to check out their [installation guide](https://selenium-python.readthedocs.io/installation.html).

## Usage

Once installed in your environment, simply type `regex_crossword` from your terminal and start playing!

### Loading level packs

When the game starts it will attempt to load "level packs" for it to use. It looks for them in the following places in descending order:

1. First, it will look wherever the `--level-packs` option was pointing when invoking the game command (for a full list of all commands use the `-h` or `--help` flag).
1. If no option was specified, it will look wherever the `REGEXCW_LEVEL_PACKS` environment variable is pointing, if it exists.
1. Lastly and by default, it will search for a directory called `level_packs` in the current working directory.

If all of this fails (or the directory has no packs), an error will pop up informing you no level packs were found.

### Getting level packs

When trying to get level packs you have several options:

- Use the `--scrape` flag (this requires you to install the `scraper` extra). This will scrape some online resources and create level packs based on them for you to load into the offline version.
- Create your own level packs!

#### Creating your own level packs

Level packs are simply JSON files who follow this format:
```json
[
    {
        "title": "Beatles",
        "up_to_down": [
            "[^SPEAK]+",
            "EP|IP|EF"
        ],
        "left_to_right": [
            "HE|LL|O+",
            "[PLEASE]+"
        ],
    },
    {
        "title": "Pisco Sour",
        "up_to_down": [
            "(MA|LM)",
            "[^MESH]+"
        ],
        "left_to_right": [
            "[LINE]+",
            "[LAM]+"
        ],
        "right_to_left": [
            "[ISLE]+",
            "[MALE]+"
        ],
        "down_to_up": [
            "[LAME]*",
            "[^LES]+"
        ]
    },
]
```

The main file json is a list of smaller dictionaries who each implement a "level" format:

- `title` - the title of the level.
- `up_to_down` - the regexes who will attempt to match the columns from top to bottom (specified from left to right)
- `left_to_right` - the regexes who will attempt to match the rows from left to right (specified from top to bottom)
- `down_to_up` - same as `up_to_down` but will attempt to match the columns from bottom to top.
- `right_to_left` - same as `left_to_right` but will attempt to match the rows from right to left.

## License

[MIT](LICENSE.txt)
