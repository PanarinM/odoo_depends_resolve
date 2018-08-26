#!/usr/bin/python
import argparse
from parse_dir import DirectoryParser


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
    print(dir_parser.modules)


if __name__ == '__main__':
    main()
