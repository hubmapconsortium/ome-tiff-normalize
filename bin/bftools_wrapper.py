#!/usr/bin/env python3
import re
import shlex
from argparse import ArgumentParser
from os import walk
from pathlib import Path
from subprocess import run
from typing import Iterable, Tuple

ome_tiff_pattern = re.compile(r"(?P<basename>.*)\.ome\.tif(f?)$")

bfconvert_command_template = [
    "/opt/bftools/bfconvert",
    "{source}",
    "{dest}",
]


def find_ome_tiffs(input_dir: Path) -> Iterable[Tuple[Path, Path]]:
    """
    Yields 2-tuples:
     [0] full Path to source file
     [1] output file Path (source file relative to input_dir)
    """
    for dirpath_str, _, filenames in walk(input_dir):
        dirpath = Path(dirpath_str)
        for filename in filenames:
            if ome_tiff_pattern.match(filename):
                filepath = dirpath / filename
                yield filepath, filepath.relative_to(input_dir)


def fix_ome_tiff(source: Path, dest: Path):
    command = [piece.format(source=source, dest=dest) for piece in bfconvert_command_template]
    print("Running", shlex.join(command))
    run(command)


def main(input_dir: Path):
    for source, dest in find_ome_tiffs(input_dir):
        fix_ome_tiff(source, dest)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("input_dir", type=Path)
    args = p.parse_args()

    main(args.input_dir)
