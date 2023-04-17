import pathlib
from typing import List
import os

PIPE = "|"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

FOLDER_ICON = "📁"
FILE_ICON = "📄"

FOLDER_COLOR = "\033[38;2;255;69;0m"  # orangered
FILE_COLOR = "\033[38;2;106;90;205m"  # slateblue

ICON_MAP = {
    "LICENSE": ("📜", "\033[38;2;176;196;222m"),  # lightsteelblue
    "README.md": ("📚", "\033[38;2;218;165;32m"),  # goldenrod
    "requirements.txt": ("🔧", "\033[38;2;220;20;60m"),  # crimson
    "setup.py": ("🛠️", "\033[38;2;173;255;47m"),  # greenyellow
    "__init__.py": ("🔹", "\033[38;2;123;104;238m"),  # mediumslateblue
}

RESET_COLOR = "\033[0m"


class DirectoryTree:
    """Initialize the DirectoryTree class.

       Args:
           root_dir (str): The root directory of the tree.
           dir_only (bool, optional): Generate a directory-only tree. Defaults to False.
           output_file (str, optional): The output file to save the tree. Defaults to "output.md".
       """
    def __init__(self, root_dir: str, dir_only: bool = False, output_file: str = "output.md"):
        """Initialize the DirectoryTree class."""
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self) -> None:
        """Generate the directory tree and save it to the output file."""
        tree = self._generator.build_tree(with_colors=False)  # Remove colors when saving to file
        markdown_output = self.generate_markdown(tree)
        if isinstance(self._output_file, str):
            with open(self._output_file, "w", encoding="utf-8") as file:
                file.write(markdown_output)
        else:
            print(markdown_output)

    def generate_markdown(self, tree: List[str]) -> str:
        """Convert the tree list to a formatted markdown string.

        Args:
            tree (List[str]): The list representing the directory tree.

        Returns:
            str: The formatted markdown string.
        """
        markdown_template = "```\n{}\n```"
        content = "\n".join(tree)
        return markdown_template.format(content)

    def generate_as_string(self, with_colors=True):
        """Generate the directory tree and return it as a string.

        Args:
            with_colors (bool, optional): Generate the tree with colors. Defaults to True.

        Returns:
            str: The directory tree as a string.
        """
        tree = self._generator.build_tree(with_colors=with_colors)
        return '\n'.join(tree)  # Use actual newline characters


class _TreeGenerator:
    """Initialize the _TreeGenerator class.

        Args:
            root_dir (str): The root directory of the tree.
            dir_only (bool, optional): Generate a directory-only tree. Defaults to False.
        """

    def __init__(self, root_dir: str, dir_only: bool = False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = []

    def build_tree(self, with_colors=True):
        """Build the directory tree.

        Args:
            with_colors (bool, optional): Generate the tree with colors. Defaults to True.

        Returns:
            List[str]: The list representing the directory tree.
        """
        self._tree_head(with_colors)
        self._tree_body(self._root_dir, with_colors=with_colors)
        return self._tree

    def _tree_head(self, with_colors):
        """Generate the header of the directory tree.

        Args:
            with_colors (bool): Generate the header with colors.
        """
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix="", with_colors=True):
        """Generate the body of the directory tree.

        Args:
            directory (Path): The current directory being processed.
            prefix (str, optional): The prefix for the current directory. Defaults to "".
            with_colors (bool, optional): Generate the body with colors. Defaults to True.
        """
        entries = self.prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector, with_colors
                )
            else:
                self._add_file(entry, prefix, connector, with_colors)
        if entries_count > 0:
            self._tree.append(prefix.rstrip())  # Only append empty line if there are more directories

    def prepare_entries(self, directory):
        """Prepare the entries in the directory for processing.

        Args:
            directory (Path): The current directory being processed.

        Returns:
            List[Path]: The list of entries in the directory.
        """
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    def _add_directory(self, directory, index, entries_count, prefix, connector, with_colors):
        """Add a directory entry to the tree.

        Args:
            directory (Path): The directory entry to add.
            index (int): The index of the directory entry in the list of entries.
            entries_count (int): The total number of entries in the list.
            prefix (str): The prefix for the current directory.
            connector (str): The connector character for the current directory.
            with_colors (bool): Generate the directory entry with colors.
        """
        if with_colors:
            self._tree.append(
                f"{prefix}{connector} {FOLDER_COLOR}{directory.name}{os.sep}{RESET_COLOR}"
            )
        else:
            self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")

        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
            with_colors=with_colors,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector, with_colors):
        """Add a file entry to the tree.

        Args:
            file (Path): The file entry to add.
            prefix (str): The prefix for the current file.
            connector (str): The connector character for the current file.
            with_colors (bool): Generate the file entry with colors.
        """
        icon, file_color = ICON_MAP.get(file.name, (FILE_ICON, FILE_COLOR))
        if with_colors:
            self._tree.append(f"{prefix}{connector} {file_color}{icon} {file.name}{RESET_COLOR}")
        else:
            self._tree.append(f"{prefix}{connector} {icon} {file.name}")
