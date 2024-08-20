import argparse
import tqdm

from profusion import Bloom

from .utils import count_lines


class Dedupe:
    def __init__(
        self,
        input_file: str,
        progress: bool = False,
    ):
        self.input_file = input_file
        self.total_lines = count_lines(input_file)
        self.progress = progress

    def dedupe(self, output_file: str, error_ratio: float = 1e-5):
        # Bloom filter
        capacity = max(self.total_lines, 1000000)
        bf = Bloom(capacity=capacity, error_ratio=error_ratio)

        unique_lines = 0
        duplicates = 0

        with open(self.input_file, "r") as in_file, open(
            output_file, "w"
        ) as out_file:
            if self.progress:
                pbar = tqdm.tqdm(
                    total=self.total_lines, desc="Processing", unit="lines"
                )

            for line in in_file:
                stripped_line = line.strip()
                if not bf.check_then_add(stripped_line):
                    out_file.write(line)  # Write original line with newline
                    unique_lines += 1
                else:
                    duplicates += 1

                if self.progress:
                    pbar.update(1)
                    pbar.set_postfix(
                        {
                            "Unique": unique_lines,
                            "Dupes": duplicates,
                        }
                    )

            if self.progress:
                pbar.close()

        # Print deduplication stats
        if self.total_lines == 0:
            ratio = 0
        else:
            ratio = unique_lines / self.total_lines

        if self.progress:
            print(f"Deduped {self.total_lines}")
            print(f"Unique lines: {unique_lines}")
            print(f"Duplicates removed: {duplicates}")
            print(f"Deduplication ratio: {ratio:.2%}")


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicate lines in a large text file."
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar during deduplication",
    )
    parser.add_argument(
        "--error_ratio",
        type=float,
        default=1e-5,
        help="Error ratio for the Bloom filter (default: 1e-5)",
    )

    args = parser.parse_args()

    deduper = Dedupe(args.input_file, progress=args.progress)
    deduper.dedupe(args.output_file, error_ratio=args.error_ratio)


if __name__ == "__main__":
    main()
