import setuptools

INSTALL_REQUIRES = ["pathlib", "colorama"]

setuptools.setup(
    name="treesnek",
    author="@al-ce",
    description="Tree-Snek - a shameless clone of tree written in Python",
    url="https://github.com/al-ce/tree-snek",
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    # packages=["poker_win_calculator"],
    python_requires=">=3.7",
    # setup.py is in the root directory of the project, but cli.py is in the
    # poker_win_calculator directory. So we need to specify the directory
    # containing cli.py
    entry_points={"console_scripts": ["treesnek=treesnek.tree:main"]},
    version="0.1.0",
)
