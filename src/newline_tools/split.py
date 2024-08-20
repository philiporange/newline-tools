import argparse
import os
from math import ceil

from .utils import count_lines


class Split:
    def __init__(
        self, input_file: str, output_prefix: str = None, progress=False
    ):
        self.input_file = input_file
        self.total_lines = count_lines(input_file)
        self.output_prefix = output_prefix or os.path.splitext(input_file)[0]
        self.progress = progress

    def _generate_output_filename(self, index: int) -> str:
        base, ext = os.path.splitext(self.output_prefix)
        return f"{base}-{index}{ext}"

    def split_by_parts(self, n: int):
        lines_per_file = ceil(self.total_lines / n)
        self._split_file(lines_per_file)

    def split_by_size(self, size: int):
        self._split_file(size)

    def _split_file(self, lines_per_file: int):
        with open(self.input_file, "r") as infile:
            file_index = 0
            line_count = 0
            outfile = None

            for line in infile:
                if line_count % lines_per_file == 0:
                    if outfile:
                        outfile.close()
                    outfile = open(
                        self._generate_output_filename(file_index), "w"
                    )
                    file_index += 1

                outfile.write(line)
                line_count += 1

            if outfile:
                outfile.close()


def main():
    parser = argparse.ArgumentParser(
        description="Split a large text file into multiple files."
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("-o", "--output", help="Output file prefix")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", type=int, help="Split into N files")
    group.add_argument(
        "-s", "--size", type=int, help="Split into files of SIZE lines each"
    )
    group.add_argument(
        "-p", "--progress", action="store_true", help="Show progress bar"
    )

    args = parser.parse_args()

    splitter = Split(args.input_file, args.output, args.progress)

    if args.n:
        splitter.split_by_parts(args.n)
    elif args.size:
        splitter.split_by_size(args.size)


if __name__ == "__main__":
    main()
