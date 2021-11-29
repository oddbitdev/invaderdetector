import unittest

from generic_algos import GenericAlgos
from invaders import Invader
from detection_algo import DetectionAlgo
from radar_map import RadarMap


def get_mock_radar_map(width, height, character):
    mock_radar_data = (character * width + "\n") * height
    return RadarMap(mock_radar_data)


def get_invaders():
    i1 = """
    --oo--
    -oooo-
    --oo--
    -o--o-
    """
    invader_1 = Invader("invader_1", i1)

    i2 = """
    o----o
    -o--o-
    -o--o-
    --oo--
    """
    invader_2 = Invader("invader_2", i2)
    return [invader_1, invader_2]


class TestRadarMap(unittest.TestCase):
    def test_enlarged_radar_data(self):
        """
        Tests that the get_enlarged_radar data method
        returns a radar data array of the correct size.
        """
        # create a five by five radar data map
        rm = get_mock_radar_map(5, 5, "-")
        # create a four by four pattern used to get the
        # enlarged radar data array
        pattern = ["-" * 4 for _ in range(4)]
        erd = rm.get_enlarged_radar_data(pattern)
        # check size of enlarged_radar_data is nine by nine
        self.assertEqual(len(erd[0]), 9)
        self.assertEqual(len(erd), 9)

    def test_get_size_window_on_no_enlarged_radar_data(self):
        """
        Tests get_size_window when no extra radar_data argument
        is provided.
        """
        # create a ten by ten radar data map
        rm = get_mock_radar_map(10, 10, "-")
        # get a window of four by four
        sw = rm.get_size_window((4, 4), (0, 0))
        # assert window size to be four by four
        self.assertEqual(len(sw[0]), 4)
        self.assertEqual(len(sw), 4)

    def test_get_size_window_on_provided_enlarged_radar_data(self):
        """
        Tests get_size_window when no extra radar_data argument
        is provided.
        """
        # create a five by five radar data map
        rm = get_mock_radar_map(5, 5, "-")
        # create an enlarged ten by ten radar data map
        # populate it with a differen character to check
        # that the get_size_window method fetches data
        # from it and not the RadarMap self radar_data
        mock_enlarged_radar_data = ["x" * 10 for _ in range(10)]
        # get a window of four by four from the enlarged radar data
        sw = rm.get_size_window((4, 4), (0, 0), mock_enlarged_radar_data)
        # assert window size to be four by four
        self.assertEqual(len(sw[0]), 4)
        self.assertEqual(len(sw), 4)
        # assert window is from enlarged radar data
        self.assertEqual(sw[0][0], "x")

    def test_size_window_when_near_bounds(self):
        """
        Tests that get_size_window returns a window
        of smaller size when the offset plus window
        size exceeds the size of the radar data.
        So requesting a window of width 4 from a
        radar map of width 8 at offset 6 will return
        a window of width 2.
        """
        # create a eight by eight radar data map
        rm = get_mock_radar_map(8, 8, "-")
        # get a window of four by four with an x offset of 6
        sw = rm.get_size_window((4, 4), (6, 0))
        # assert window size to be two by four
        self.assertEqual(len(sw[0]), 2)
        self.assertEqual(len(sw), 4)

    def test_value_error_on_negative_offsets(self):
        """
        Tests that a ValueError is raised when negative
        offsets are provided to get_size_window.
        """
        # create a five by five radar data map
        rm = get_mock_radar_map(5, 5, "-")
        # check for ValueError on negative offsets
        with self.assertRaises(ValueError):
            rm.get_size_window((2, 2), (-1, -1))

    def test_value_error_on_window_larger_than_map(self):
        """
        Tests that a ValueError is raised when the requested
        window size is larger than the radar data.
        """
        # create a five by five radar data map
        rm = get_mock_radar_map(5, 5, "-")
        # check for ValueError when requesting a window
        # larger than the radar data 
        with self.assertRaises(ValueError):
            rm.get_size_window((6, 6), (0, 0))

class TestGenericAlgos(unittest.TestCase):

    def test_levenshtein(self):
        """
        Values compared against python-Levenshtein library results.
        """
        ga = GenericAlgos()
        d, r = ga.levenshtein("abc", "abc")
        self.assertEqual(d, 0)
        self.assertEqual(r, 1.0)
        d, r = ga.levenshtein("abcd", "abxd")
        self.assertEqual(d, 1)
        self.assertEqual(r, 0.75)
        d, r = ga.levenshtein("abcd", "abx")
        self.assertEqual(d, 2)
        self.assertAlmostEqual(r, 0.5714285714)

    def test_run_leven(self):
        """
        Tests run_leven on a list of strings.
        """
        ga = GenericAlgos()
        s1 = s2 = ["abc", "def", "ghi"]
        result = ga.run_leven(s1, s2)
        self.assertEqual(len(result), 3)
        for r in result:
            self.assertEqual(r, (0, 1.0))

    def test_compare_input_data_to_pattern(self):
        """
        Tests the comparison of input data to pattern,
        score should be 1.0 on the same pattern.
        """
        ga = GenericAlgos()
        input_data = pattern = ["abc", "def", "ghi"]
        result = ga.compare_input_data_to_pattern(input_data, pattern)
        self.assertEqual(result, 1.0)

    def test_find_peaks_on_zero_threshold(self):
        """
        Tests find peaks with zero threshold.
        """
        ga = GenericAlgos()
        result = ga.find_peaks([[3, 4, 1, 5, 6, 3, 3, 7, 1, 2]])
        self.assertEqual(result, [[0, 4, 0, 0, 6, 0, 0, 7, 0, 2]])

    def test_find_peaks_on_non_zero_threshold(self):
        """
        Tests find peaks with a non zero threshold.
        """
        ga = GenericAlgos()
        ga.threshold = 4
        result = ga.find_peaks([[3, 4, 1, 5, 6, 3, 3, 7, 1, 2]])
        self.assertEqual(result, [[0, 0, 0, 0, 6, 0, 0, 7, 0, 0]])


class TestDetectionAlgo(unittest.TestCase):

    def test_with_no_overlaps(self):
        rd = """
        ---oo---------------
        --oooo---o----o-----
        ---oo-----o--o------
        --o--o----o--o------
        -----------oo-------
        --------------------
        """
        
        invaders = get_invaders()
        
        rm = RadarMap(rd)
        da = DetectionAlgo(rm, invaders, 0.9)
        candidates = da.run_search()
        self.assertEqual(len(candidates), 2)

    def test_with_overlaps(self):
        rd = """
        ---oo----------------------
        --oooo---o------o----o-----
        ---oo---o--------o--o------
        --o--o--o--------o--o------
        ------oo----------oo-------
        ---------------------------
        """
        
        invaders = get_invaders()
        
        rm = RadarMap(rd)
        da = DetectionAlgo(rm, invaders, 0.8)
        candidates = da.run_search()
        self.assertEqual(len(candidates), 2)
        # check position of detcted invaders
        for invader in candidates:
            if invader.name == "invader_1":
                self.assertEqual(invader.real_x, 1)
                self.assertEqual(invader.real_y, 0)
            if invader.name == "invader_2":
                self.assertEqual(invader.real_x, 16)
                self.assertEqual(invader.real_y, 1)
