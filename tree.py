"""
Print out the structure of the current directory.

root/
├── sub1/
│   ├── sub2/
│   │   ├── file1.txt
│   │   └── file2.txt
│   └── file4.txt
├── sub4/
│   └── file5.txt
└── file6.txt
"""

from pathlib import Path
from colorama import Fore

PIPE = '│'
PIPE_EXT = '│   '
ELBOW = '└── '
TEE = '├── '
CORNER = '└'
HIDE_LIST_PREFIXES = ('__', '.')


class TreeGrower():

    def __init__(self, path, hide=True, max_indent=float('inf')):
        self.path = Path(path)
        self.hide = hide
        self.max_indent = max_indent

    def is_hidden(self, path_obj: Path, hide: bool) -> bool:
        """Return True if the Path obj is hidden and hide flag is True."""
        return hide and path_obj.name.startswith(HIDE_LIST_PREFIXES)

    def path_data(self, path, hide=True, root=True) -> dict:
        """Return a dictionary of the path's contents."""
        data = {'name': path.name}
        if root:
            data['root'] = True
        if path.is_dir():
            data['type'] = 'directory'
            data['contents'] = \
                [self.path_data(child, hide, False)
                 for child in path.iterdir()
                 if not self.is_hidden(child, hide)]
            return data

        return {'type': 'file',
                'extension': path.suffix[1:],
                'size': path.stat().st_size} | data

    def sorting_key(self, item): return item['type'], item['name']

    def sort_dict(self, d: dict) -> dict:
        """Sort the dictionary by type then name."""

        d['contents'] = sorted(d['contents'], key=self.sorting_key)

        [self.sort_dict(item)
         for item in d.get('contents')
         if item['type'] == 'directory']

        return d

    def colorize(self, string: str, color=Fore.BLUE) -> str:
        return f"{color}{string}{Fore.RESET}"

    def generate_tree(self, d, max_indent=float('inf'), indent=0) -> list:
        """Return a list of strings that represent the tree."""

        branch = [self.colorize('./')] if d.get('root') else []

        if d['type'] != 'directory' or indent >= max_indent:
            return branch

        d_contents = d['contents']
        last_item = len(d_contents) - 1

        for i, item in enumerate(d_contents):
            extension = f'{PIPE_EXT}' * indent
            stem = ELBOW if i == last_item else TEE
            name = item['name']
            slash, name = ('/', self.colorize(name)
                           ) if item['type'] == 'directory' else ('', name)

            branch += [f"{extension}{stem}{name}{slash}"] + \
                    self.generate_tree(item, max_indent, indent + 1)  # noqa
        return branch

    def prune_tree(self, tree):
        """Remove any branches that go nowhere."""
        new_tree = []
        for i, line in enumerate(tree):
            new_line = ""
            for j, char in enumerate(line):
                to_prune = char == PIPE and (
                    # Looks at char directly above the current char
                    tree[i - 1][j] == CORNER or new_tree[i - 1][j] == ' ')

                char = ' ' if to_prune else char
                new_line += char
            new_tree.append(new_line)

        return new_tree

    def __repr__(self):
        """Return the tree as a string."""
        data = self.path_data(self.path, self.hide)
        sorted_data = self.sort_dict(data)
        tree = self.generate_tree(sorted_data, self.max_indent)
        tree = self.prune_tree(tree)
        return "\n".join(tree)


def main():
    root = Path.cwd()
    root_str = str(root)
    root = TreeGrower(root_str, True, 5)

    print(root.__repr__())


if __name__ == '__main__':
    main()
