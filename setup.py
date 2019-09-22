import typing

import setuptools


def _get_long_description_data() -> typing.Tuple[str, str]:
    """
    Get data regarding the long description of the package.

    :return: tuple of the README.md text and the long_description type.
    :rtype: typing.Tuple[str, str]
    """
    with open('README.md', 'r') as readme:
        return (readme.read(), 'text/markdown')


LONG_DESCRIPTION, LONG_DESCRIPTION_CONTENT_TYPE = _get_long_description_data()

setuptools.setup(
    name='regex_crossword',
    version='0.1.0',
    description='A Python implementation of a Regex Crossword in the terminal.',
    url='https://github.com/DivoK/regex_crossword',
    author='Divo Kaplan',
    author_email='divokaplan@gmail.com',
    python_requires='>=3.7',
    packages=setuptools.find_packages(),
    include_package_data=True,
    extras_require={'scraper': ['selenium', 'beautifulsoup4', 'loguru']},
    entry_points='''
        [console_scripts]
        regex_crossword=regex_crossword.scripts.regex_crossword:cli
    ''',
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    keywords='terminal curses game regex crossword educational',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Topic :: Education',
        'Topic :: Games/Entertainment :: Puzzle Games',
    ],
)
