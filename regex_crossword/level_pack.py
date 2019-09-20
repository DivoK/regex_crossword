import json
from pathlib import Path

from .level import Level


class LevelPack:
    def __init__(self, path: Path):
        self.title = str(path.stem)
        self._raw_data = json.loads(path.read_text())
        self.levels = [Level(lvl) for lvl in self._raw_data]

    def __iter__(self):
        return iter(self.levels)
