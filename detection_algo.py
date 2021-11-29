from abc import ABC, abstractmethod
from typing import List

from generic_algos import GenericAlgos
from invaders import Invader, InvaderMatch
from radar_map import RadarMap


class BaseDetectionAlgo(ABC):
    """
    Base abstract class for the invader detection algorithm.
    """

    @abstractmethod
    def run_search(self):
        pass


class DetectionAlgo(BaseDetectionAlgo, GenericAlgos):
    """
    Levenshtein distance based detection algorithm.
    It works by scanning every cell in the radar data with a
    window the size of a given invader, then comparing the
    Levenshtein ratio of every row and column, averaging out
    the values and leaving only matches greated than a specified
    threshold.
    Overlapping candidates are also filtered on the highest score.
    """

    def __init__(
        self, radar_map: RadarMap, invaders: List[Invader], threshold: float
    ) -> None:
        self.radar_map = radar_map
        self.invaders = invaders
        self.threshold = threshold

    def scan_radar_data(self, pattern: List[str]):
        """
        Given an invader pattern the method will get an enlarged radar_data
        base on the pattern and scan it by row and column on windows the
        size of the pattern and assigning each coordinate a match score.
        """
        enlarged_radar_data = self.radar_map.get_enlarged_radar_data(pattern)
        p_h = len(pattern)
        p_w = len(pattern[0])
        scores = []
        for j in range(len(enlarged_radar_data) - p_h):
            row_scores = []
            for i in range(len(enlarged_radar_data[0]) - p_w):
                window = self.radar_map.get_size_window(
                    (p_w, p_h), (i, j), enlarged_radar_data
                )
                row_scores.append(self.compare_input_data_to_pattern(window, pattern))
            scores.append(row_scores)
        return scores

    def get_targets_from_scan_data(self, invader: Invader) -> List[InvaderMatch]:
        """
        Run the invader patter on the radar data, filter and keep
        the peaks with the best matching scores and return a
        list of all matching invaders.
        """
        pattern = invader.pattern
        # scan radar data to obtain a matrix of match scores
        rs = self.scan_radar_data(pattern)
        # filter peaks for rows
        sp = self.find_peaks(rs)
        # transpose matrix and filter peaks for columns
        sp = self.find_peaks(zip(*sp))
        # transpose the matrix back
        sp = list(zip(*sp))
        x_half = int(len(pattern[0]) / 2)
        y_half = int(len(pattern) / 2)
        matching_invaders = []
        for j, row in enumerate(sp):
            for i, cel in enumerate(row):
                if cel > 0:
                    # account for enlarged radar map coordinates
                    real_x_coord = max(0, i - x_half)
                    real_y_coord = max(0, j - y_half)
                    m = InvaderMatch(
                        invader.name,
                        i,
                        j,
                        real_x_coord,
                        real_y_coord,
                        invader.width,
                        invader.height,
                        cel,
                    )
                    matching_invaders.append(m)
        return matching_invaders

    def overlap(self, m1: InvaderMatch, m2: InvaderMatch) -> bool:
        """
        Checks over two invaders overlap, basically checks for
        rectangle collission.
        """
        if m1.x > m2.x + m2.width or m1.x + m1.width < m2.x:
            return False
        if m1.y > m2.y + m2.height or m1.y + m1.height < m2.y:
            return False
        return True

    def get_overlaps(
        self, match: InvaderMatch, matches: List[InvaderMatch]
    ) -> List[InvaderMatch]:
        """
        Given an invader to match against and a list of invders
        the method will return all overlapping invaders.
        """
        overlaps = []
        for m in matches:
            if self.overlap(match, m):
                overlaps.append(m)
        return overlaps

    def get_best_matching_data(
        self, invader_coord_scores: List[InvaderMatch]
    ) -> List[InvaderMatch]:
        """
        Given a list of invaders, their coordinates and match scores
        in case of invader overlaps the method will select the invader
        with the highest score, otherwise will just insert the invader
        in the final list.
        """
        final_matches = set()
        excluded = set()
        for match in invader_coord_scores:
            if match in excluded:
                continue
            overlaps = self.get_overlaps(match, invader_coord_scores)
            if overlaps:
                best_score_match = max(overlaps, key=lambda m: m.score)
                final_matches.add(best_score_match)
                overlaps.remove(best_score_match)
                (excluded.add(o) for o in overlaps)
            else:
                final_matches.add(match)
        return list(final_matches)

    def run_search(self) -> List[InvaderMatch]:
        """
        Main entry function to search for invader patterns.
        """
        matching_data = []
        for invader in self.invaders:
            md = self.get_targets_from_scan_data(invader)
            matching_data += md
        return self.get_best_matching_data(matching_data)
