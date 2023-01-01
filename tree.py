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


def is_hidden(path_obj: Path, hide: bool) -> bool:
    """Return true if the Path obj is hidden and the user wants to hide it."""
    return hide and path_obj.name.startswith(HIDE_LIST_PREFIXES)


def path_data(path, hide=True, root=True) -> dict:
    """Return a dictionary of the path's contents."""
    data = {'name': path.name}
    if root:
        data['root'] = True
    if path.is_dir():
        data['type'] = 'directory'
        data['contents'] = \
            [path_data(child, hide, False)
             for child in path.iterdir() if not is_hidden(child, hide)]
        return data

    return data | {'type': 'file',
                   'extension': path.suffix[1:], 'size': path.stat().st_size}


def sort_dict(d: dict) -> dict:
    """Sort the dictionary by type then name."""

    d['contents'] = sorted(d['contents'], key=lambda x: (x['type'], x['name']))
    [sort_dict(item) for item in d['contents'] if item['type'] == 'directory']
    return d


def colorize(name: str) -> str:
    """Color the name of the directory."""
    return f"{Fore.BLUE}{name}{Fore.RESET}"


def generate_tree(d, max_indent=float('inf'), indent=0) -> list:
    """Return a list of strings that represent the tree."""
    branch = [colorize('./')] if d.get('root') else []

    if d['type'] != 'directory' or indent >= max_indent:
        return branch

    d_contents = d['contents']
    last_item = len(d_contents) - 1

    for i, item in enumerate(d_contents):
        extension = f'{PIPE_EXT}' * indent
        stem = ELBOW if i == last_item else TEE
        name = item['name']
        slash, name = ('/', colorize(name)
                       ) if item['type'] == 'directory' else ('', name)

        branch += [f"{extension}{stem}{name}{slash}"] + \
                   generate_tree(item, max_indent, indent + 1)  # noqa
    return branch


def prune_tree(tree):
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


def main():
    root = Path.cwd()
    dir_contents = sort_dict(path_data(root))
    tree = generate_tree(dir_contents)
    tree = prune_tree(tree)

    [print(branch) for branch in tree]


if __name__ == '__main__':
    main()
