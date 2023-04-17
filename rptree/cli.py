"""This module provides RP Tree CLI."""

import argparse
import sys
import pathlib

from . import __version__
from .rptree import DirectoryTree


def parse_cmd_line_arguments():
    """Parse the command
        -line arguments for the RP Tree CLI.
    Returns:
        argparse.
    Namespace
        : The parsed command-line arguments.
    """
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
    """The main entry point for the RP Tree CLI. It parses the command-line arguments,
    validates the provided root directory, and generates the directory tree based on the
    specified options.
    """
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print(f"{root_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    tree = DirectoryTree(args.root_dir, dir_only=args.dir_only, output_file=args.output_file)
    if args.as_string:
        tree_string = tree.generate_as_string(with_colors=False)
        print(tree_string)
    else:
        tree.generate()

