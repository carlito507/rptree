"""This module provides RP Tree CLI."""

import argparse
import os
import sys
import pathlib

from . import __version__
from .rptree import DirectoryTree


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        description="RP Tree CLI",
        epilog="RP Tree CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Print version information",
    )
    parser.add_argument(
        "root_dir",
        type=str,
        help="The root directory of the tree",
    )
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a directory-only tree",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        help="Generate a full directory tree and save it to a file",
    )
    parser.add_argument(
        "-s",
        "--as-string",
        action="store_true",
        help="Generate a full directory tree and return it as a string",
    )
    return parser.parse_args()


def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        raise ValueError(f"{root_dir} is not a directory")
        sys.exit()
    tree = DirectoryTree(root_dir, dir_only=args.dir_only, output_file=args.output_file, as_string=False)
    tree.generate()
