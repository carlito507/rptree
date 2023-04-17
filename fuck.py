
class _TreeGenerator:
    def __init__(self, root_dir: str, dir_only: bool = False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = []

    def build_tree(self, with_colors=True):
        self._tree_head(with_colors)
        self._tree_body(self._root_dir, with_colors=with_colors)
        return self._tree

    def _tree_head(self, with_colors):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix="", with_colors=True):
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

    def prepare_entries(self, directory):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    def _add_directory(self, directory, index, entries_count, prefix, connector, with_colors):
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
        icon, file_color = ICON_MAP.get(file.name, (FILE_ICON, FILE_COLOR))
        if with_colors:
            self._tree.append(f"{prefix}{connector} {file_color}{icon} {file.name}{RESET_COLOR}")
        else:
            self._tree.append(f"{prefix}{connector} {icon} {file.name}")
