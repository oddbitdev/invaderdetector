from typing import List, Optional, Tuple


class RadarMap:
    """
    Class that represents the radar data and the operations
    that can be performed on it.
    """

    def __init__(self, radar_data: List[str], empty_char: str = "-") -> None:
        self.radar_data = radar_data.split()
        self.empty_char = empty_char

    def get_enlarged_radar_data(self, pattern: List[str]) -> List[str]:
        """
        Given a pattern the method will return an enlarged map
        with each margin having extra padding of half the size
        of the pattern with the empty character.
        """
        half_width = int(len(pattern[0]) / 2)
        half_height = int(len(pattern) / 2)
        top_bottom = [
            self.empty_char * (len(self.radar_data[0]) + len(pattern[0]))
            for _ in range(half_height)
        ]
        enlarged_radar_data = []
        enlarged_radar_data.extend(top_bottom)
        for row in self.radar_data:
            enlarged_radar_data.append(
                self.empty_char * half_width + row + self.empty_char * half_width
            )
        enlarged_radar_data.extend(top_bottom)
        return enlarged_radar_data

    def get_size_window(
        self,
        size: Tuple[int, int],
        offset: Tuple[int, int],
        radar_data: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Returns a window of a given size from a specific offset
        from radar_data.
        Optionally it can take another radar_data map (like an enlarged one)
        and process that.
        """
        if radar_data is None:
            radar_data = self.radar_data

        width = size[0]
        height = size[1]
        x_offset = offset[0]
        y_offset = offset[1]
        # do not allow negative offsets
        if x_offset < 0 or y_offset < 0:
            raise ValueError("Negative offsets provided!")
        # do not allow windows larger than radar_data
        if width > len(radar_data[0]) or height > len(radar_data):
            raise ValueError("Window size larger than radar data!")
        y_data = radar_data[y_offset : y_offset + height]
        window = []
        for line in y_data:
            window.append(line[x_offset : x_offset + width])
        return window
