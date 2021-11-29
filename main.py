import argparse

import os
import sys

from loader import Loader
from detection_algo import DetectionAlgo

parser = argparse.ArgumentParser(description="List the content of a folder")

# Add the arguments
parser.add_argument("Path", metavar="path", type=str, help="the path to list")

parser.add_argument(
    "--threshold", action="store", type=float, required=True, help="threshold value"
)

args = parser.parse_args()

input_path = args.Path

if __name__ == "__main__":
    if not os.path.isdir(input_path):
        print("The path specified does not exist")
        sys.exit()
    loader = Loader(input_path)
    radar_map, invaders = loader.load_data()
    algo = DetectionAlgo(radar_map, invaders, 0.82)

    results = algo.run_search()

    print(f"Found {len(results)} candidates:")
    for i in results:
        print(
            f"Candidate: {i.name} at {i.real_x}, {i.real_y} with score {i.score: .2f}"
        )
        print(
            "\n".join(
                radar_map.get_size_window((i.width, i.height), (i.real_x, i.real_y))
            )
        )
