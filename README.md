# invaderdetector

Levenshtein distance based detection of invader patterns in a given map of data, accounting for noise in the signal.
Given a list of invader patterns and a map of data to search, the algorithm works by going through each invader and enlarging the given map data on the map edges based on that invader (adding the background character "-": columns of invader_width/2 on the left/right of map and rows of invader_height/2 top/bottom) in order to accound for patterns near the edge or the map data.

Then for each cell in the map data it scans a window of the invader's dimensions and assigns it a score provided it exceeds a given threshold.

The score is calculated by averaging the Levenshtein ratio for each row and column when comparing the invader pattern to the scanned window.

After all potential detection sites have been scanned the algorithm then checks for overlaps between candidates and picks those with the highest score.

Current implementation expects invader patterns and map data to be provided in text files with "radar_data" and "invader" in their names.

Tested with Python3.9. Current implementation takes a path argument to the directory containing the invader patterns and radar data, and a threshold argument:

`python main.py /path/to/input_files --threshold 0.82`

Run tests with:

`python -m unittest tests.py`
