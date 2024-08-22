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
        if self.total_lines == 0:
            return

        lines_per_file = [ceil(self.total_lines / n)] * n
        self._split_file(lines_per_file)

    def split_by_size(self, size: int):
        if self.total_lines == 0:
            return

        n = ceil(self.total_lines / size)
        lines_per_file = [size] * (n - 1) + [self.total_lines - size * (n - 1)]
        self._split_file(lines_per_file)

    def split_by_proportion(self, proportions: list):
        if self.total_lines == 0:
            return

        # Normalize proportions
        total = sum(proportions)
        proportions = [p / total for p in proportions]

        lines_per_file = [round(p * self.total_lines) for p in proportions]
        # Adjust the last file to account for rounding errors
        lines_per_file[-1] = self.total_lines - sum(lines_per_file[:-1])
        self._split_file(lines_per_file)

    def _split_file(self, lines_per_file: list):
        with open(self.input_file, "r") as infile:
            file_index = 0
            line_count = 0

            for lines in lines_per_file:
                with open(
                    self._generate_output_filename(file_index), "w"
                ) as outfile:
                    for _ in range(lines):
                        line = infile.readline()
                        if not line:  # End of file
                            break
                        outfile.write(line)
                        line_count += 1

                file_index += 1

                if line_count >= self.total_lines:
                    break
