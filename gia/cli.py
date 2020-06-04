import argparse
from pathlib import Path

from .aggregator import ImageAggregator


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('destination', type=str,
                        help='ABSOLUTE path for where your images should be downloaded')
    parser.add_argument('classes', type=str,
                        help='a python list in a string of the classes for the queries')
    parser.add_argument("queries", type=str,
                        help='a python list of lists in a string of the queries corresponding to each class')
    parser.add_argument('--depth', '-d', type=int,
                        help='the default depth to go through queries for images')

    """decompressed example fish command
    gia (wslpath -w (pwd)/data) 
        "[
            'jeff bezos', 
            'bill gates'
        ]" 
        "[
            ['jeff bezos', ['jeff bezos face', 2]], 
            ['bill gates', ['bill gates face', 2]]
        ]" 
        --depth 0
    """

    args = parser.parse_args()

    destination = args.destination
    classes = eval(args.classes)
    queries = eval(args.queries)
    depth = args.depth

    if depth is None:
        depth = 0

    ia = ImageAggregator(destination, classes, queries, default_depth=depth)
    ia.aggregate()
    
if __name__ == "__main__":
    main()