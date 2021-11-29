from pathlib import Path
from typing import List, Tuple
from radar_map import RadarMap
from invaders import Invader


class Loader:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.radar_pattern = "radar_data"
        self.invader_pattern = "invader"

    def load_data(self) -> Tuple[RadarMap, List[Invader]]:
        """
        Loads radar_data and invader patterns from files in self.path
        """
        invaders = []
        for file in self.path.iterdir():
            if file.name.startswith(self.invader_pattern):
                invaders.append(Invader(file.stem, file.read_text()))
            elif file.name.startswith(self.radar_pattern):
                radar_map = RadarMap(file.read_text())
        return radar_map, invaders
