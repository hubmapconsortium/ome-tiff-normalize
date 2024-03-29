#!/usr/bin/env python3
import json
import re
import shlex
from argparse import ArgumentParser
from collections import defaultdict
from os import walk
from pathlib import Path
from subprocess import run
from typing import Iterable, Tuple

ome_tiff_pattern = re.compile(r"(?P<basename>.*)\.ome\.tif(f?)$")

bfconvert_command_template = [
    "/opt/bftools/bfconvert",
    "-bigtiff",
    "{source}",
    "{dest}",
]


def get_directory_manifest(paths: Iterable[Path]):
    listing = defaultdict(list)
    for path in paths:
        # hack
        if len(path.parts) == 1:
            directory = "."
        else:
            directory = path.parts[0]
        listing[directory].append(path)

    manifest = []
    for directory, file_paths in listing.items():
        manifest.append(
            {
                "class": "Directory",
                "path": directory,
                "basename": directory,
            }
        )

    return manifest


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


def main(input_dir: Path, output_path_prefix):
    files = []
    for source, dest_relative in find_ome_tiffs(input_dir):
        dest_absolute = output_path_prefix / dest_relative
        fix_ome_tiff(source, dest_absolute)
        files.append(dest_relative)
    with open("manifest.json", "w") as f:
        json.dump(get_directory_manifest(files), f)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("input_dir", type=Path)
    p.add_argument("--output-path-prefix", type=Path, default=Path())
    args = p.parse_args()

    main(args.input_dir, args.output_path_prefix)
