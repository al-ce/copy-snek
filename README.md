# Tree-Snek

https://user-images.githubusercontent.com/23170004/212629783-0f79299d-351c-4b44-8e4a-b4ca31df1bc3.mov

Because [treepy](https://pypi.org/project/treepy/) was already taken and does this better.

## Description

A shameless imitation of [tree](https://www.computerhope.com/unix/tree.htm) to print a nice looking recursive tree of the current directory in your terminal, but none of tree's other great opts. Just use tree! I wrote this as an exercise to learn the Python `pathlib` module.

`treesnek` "grows" the directory tree by recursively adding the directory's contents to a dictionary to the specified depth limit (`TreeGrower.path_data()`), then sorting the dictionary by type (directory or non-) then name (possible since Python 3.7).

Then it generates a tree by creating a list of strings that represent the tree (`TreeGrower.generate_tree()`) as if you were slicing the tree horizontally, adding connective branches along the way. Again, it uses recursion to reach the maximum depth set by the limit flag (`--l`), returning once it hits the limit. But, rather clumsily, it adds branches that go nowhere as it creates this list because it doesn't know if a sub-directory is the last one in its own folder until that sub-directory is done printing its own contents. That's confusing, so here's a picture of what `treesnek` would output without calling the `TreeGrower.prune_tree()` function.

<img width="290" alt="unpruned-tree" src="https://user-images.githubusercontent.com/23170004/212633338-aff0b461-35c3-41bd-9945-80b5006c7831.png">

The circled branches don't go anywhere, but I couldn't figure out an efficient way of calculating when the program should draw the vertical line. So instead, we generate the `List[str]` and then go back and "prune" it: if the char above any pipe `│` char is a corner/elbow `└` or an empty string (meaning a pipe was pruned there in the previous row), we prune that pipe, but really we're redrawing the whole tree.

<img width="427" alt="depth_demo" src="https://user-images.githubusercontent.com/23170004/212630129-028e88dd-c5c3-4224-84ae-8bdd15c0c4a9.png">

## Usage

In any directory in your terminal, use the `treesnek` command available after install.

`treesnek` takes two optional arguments:

- `--h` to show hidden files
- `--l` to control the level of directory depth to print (default 1). e.g. `treesnek --l 5`


## Requirements

Python >= 3.7 with `pip`. This program uses the `pathlib` and `colorama` modules.

## Installation

Clone this repository, `cd` into the directory, and install with `pip`.

`$ pip install .`
