from typing import List, Tuple


class GenericAlgos:
    def __init__(self) -> None:
        self.threshold = 0

    def levenshtein(self, s1: str, s2: str) -> Tuple[int, float]:
        """
        Computes the Levenshtein distance and ratio.
        Modified implementation of
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
        to include the ratio calculation.
        """
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        previous_ratio_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            ratio_row = [i + 1]
            for j, c2 in enumerate(s2):
                ratio_cost = 0 if c1 == c2 else 2
                lev_cost = 0 if c1 == c2 else 1
                insertions = (
                    previous_row[j + 1] + 1
                )  # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1  # than s2
                ratio_insertions = previous_ratio_row[j + 1] + 1
                lev_substitutions = previous_row[j] + lev_cost
                ratio_substitutions = previous_ratio_row[j] + ratio_cost
                current_row.append(min(insertions, deletions, lev_substitutions))
                ratio_row.append(min(ratio_insertions, deletions, ratio_substitutions))
            previous_row = current_row
            previous_ratio_row = ratio_row

        lev = previous_row[-1]
        r = previous_ratio_row[-1]
        ratio = ((len(s1) + len(s2)) - r) / (len(s1) + len(s2))

        return lev, ratio

    def run_leven(
        self, str_list_1: List[str], str_list_2: List[str]
    ) -> List[Tuple[int, float]]:
        """
        Runs Levenshtein distance and ratio on two lists of strings
        returning a list of the results.
        """
        leven = []
        for index, str_1 in enumerate(str_list_1):
            str_2 = str_list_2[index]
            leven.append(self.levenshtein(str_1, str_2))
        return leven

    def compare_input_data_to_pattern(
        self, input_data: List[str], pattern: List[str]
    ) -> float:
        """
        Given an input pattern and a pattern to compare it with
        the method will run a Levenshtein ratio comparison for
        each row and column, returning the average of the values.
        """
        row_leven = self.run_leven(input_data, pattern)
        t_input_data = list(map(lambda l: "".join(l), zip(*input_data)))
        t_pattern = list(map(lambda l: "".join(l), zip(*pattern)))
        col_leven = self.run_leven(t_input_data, t_pattern)
        row_score = sum([i[1] for i in row_leven]) / len(row_leven)
        col_score = sum([i[1] for i in col_leven]) / len(col_leven)
        return (row_score + col_score) / 2

    def find_peaks(self, score_data: List[List[float]]) -> List[List[float]]:
        """
        Given a list of list of floats the method will keep only the peaks
        and replace all other elements with 0, will also filter out values
        lower than a specified threshold.
        e.g.:
        given [[3, 4, 1, 5, 6, 3, 3, 7, 1, 2]] and a threshold of 0
        the result will be
        [[0, 4, 0, 0, 6, 0, 0, 7, 0, 2]]
        """
        score_peaks = []
        for data in score_data:
            prev_peak = None
            ascending = True
            peaks = []
            for index, i in enumerate(data):
                if index == 0:
                    prev_peak = i
                elif i < prev_peak and ascending:
                    if prev_peak > self.threshold:
                        peaks.append(prev_peak)
                    else:
                        peaks.append(0)
                    ascending = False
                    prev_peak = i
                else:
                    if i < prev_peak:
                        ascending = False
                    else:
                        ascending = True
                    peaks.append(0)
                    prev_peak = i
            else:
                if ascending:
                    if i > self.threshold:
                        peaks.append(i)
                    else:
                        peaks.append(0)
                else:
                    peaks.append(0)
            score_peaks.append(peaks)
        return score_peaks

