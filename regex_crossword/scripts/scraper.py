import json
import typing
from pathlib import Path

import bs4
from loguru import logger
from selenium import webdriver

ROOT_SITE = 'https://regexcrossword.com'  # Where to scrape from.
CHALLENGES_BLACKLIST = [
    'hexagonal'
]  # We just don't support some freaky challenge types. Sorry.

level_dict_type = typing.Dict[str, typing.Union[str, typing.List[str]]]
pack_dict_type = typing.Dict[str, typing.Union[str, level_dict_type]]


def parse_level(content: str) -> level_dict_type:
    """
    Parse a level's page content into a level_dict.

    :param content: the content of the level's page.
    :type content: str
    :return: dict containing the title and different regexes with their orientation.
    :rtype: level_dict_type
    """
    soup = bs4.BeautifulSoup(content, 'html.parser')
    title = soup.title.string.split('|')[0].strip()
    logger.debug(f'parsing level {title}')
    logger.debug('parsing up_to_down')
    up_to_down = [element.text for element in soup.find('thead').find_all('span')]
    logger.debug('parsing down_to_up')
    down_to_up = [element.text for element in soup.find('tfoot').find_all('span')]
    left_to_right = []
    right_to_left = []
    logger.debug('parsing tbody')
    for i, element in enumerate(soup.find('tbody').find_all('span')):
        if i % 2 == 0:
            left_to_right.append(element.text)
        else:
            right_to_left.append(element.text)
    return {
        'title': title,
        'up_to_down': up_to_down,
        'left_to_right': left_to_right,
        'right_to_left': right_to_left,
        'down_to_up': down_to_up,
    }


def parse_pack(driver: webdriver.Chrome, pack_url: str) -> pack_dict_type:
    """
    Parse the various levels in a pic into a pack_dict.

    :param driver: the current session webdriver.
    :type driver: webdriver.Chrome
    :param pack_url: main url of the pack.
    :type pack_url: str
    :return: dict tontaining the title and various levels of a pack.
    :rtype: pack_dict_type
    """
    logger.info(f'parsing pack {pack_url}')
    levels = []
    i = 1
    while True:
        logger.debug(f'parsing level {i}')
        level_url = f'{pack_url}/{i}'
        driver.get(level_url)
        try:
            levels.append(parse_level(driver.page_source))
        except Exception:
            logger.warning(f'got exception, treating pack {pack_url} as finished')
            break
        i += 1
    return {'title': pack_url.split('/')[-2], 'levels': levels}


def get_challenge_packs(content: str) -> typing.List[str]:
    """
    Return all the various challenge packs on site right now.

    :param content: the content of the page holding the packs.
    :type content: str
    :return: list of all pack urls.
    :rtype: typing.List[str]
    """
    logger.info('getting challenge packs')
    soup = bs4.BeautifulSoup(content, 'html.parser')
    return [
        element.get('href')
        for element in soup.find_all('a')
        if element.get('href').startswith('/challenges')
        and not element.get('href').split('/')[-1] in CHALLENGES_BLACKLIST
    ]


def scrape(output_path: Path) -> None:
    """
    Scrape the main root site's challenge packs and save them into output path.

    :param output_path: where to save the packs to.
    :type output_path: Path
    :return: none.
    :rtype: None
    """
    logger.info(f'start scraping on {ROOT_SITE}')
    driver = webdriver.Chrome()
    driver.get(ROOT_SITE)
    challenge_packs = get_challenge_packs(driver.page_source)
    for i, pack_route in enumerate(challenge_packs):
        pack = parse_pack(driver, f'{ROOT_SITE}{pack_route}/puzzles')
        path_to_pack = Path(output_path, f'{i}_{pack["title"]}').with_suffix('.json')
        path_to_pack.parent.mkdir(parents=True, exist_ok=True)
        path_to_pack.write_text(json.dumps(pack['levels'], indent=4))
    logger.info('done!')
