#!/usr/bin/python
import argparse
from parse_dir import DirectoryParser
from pprint import pprint


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "paths",
        nargs="*",
        help="Paths to look modules in",
    )
    args = arg_parser.parse_args()
    return args


def main():
    args = get_args()
    dir_parser = DirectoryParser(args.paths)
    result = [
        x.get_cyclic_dependencies()
        for x in dir_parser.modules
        if x.get_cyclic_dependencies()
    ]
    pprint(result)


if __name__ == '__main__':
    main()
