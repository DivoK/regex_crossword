import json
from pathlib import Path

from .level import Level


class LevelPack:
    """
    Class that serves as a container to multiple levels.
    Initialized from a path to a JSON file describing one.
    """

    def __init__(self, path: Path):
        self.title = str(path.stem)
        self._raw_data = json.loads(path.read_text())
        self.levels = [Level(lvl) for lvl in self._raw_data]

    def __iter__(self):
        return iter(self.levels)

    def __getitem__(self, index: int) -> Level:
        return self.levels[index]

    def __len__(self) -> int:
        return len(self.levels)
