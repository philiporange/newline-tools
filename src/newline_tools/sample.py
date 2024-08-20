import argparse
import random
from typing import Set

from .utils import count_lines


class Sample:
    def __init__(
        self,
        input_file: str,
        output_file: str,
        sample_size: int,
        progress: bool = False,
        seed: int = None,
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.sample_size = sample_size
        self.total_lines = count_lines(input_file)
        self.progress = progress
        self.seed = seed
        self.rng = random.Random(self.seed)

    def reservoir_sample(self):
        with open(self.input_file, "r") as infile, open(
            self.output_file, "w"
        ) as outfile:
            # If sample size is larger than total lines, adjust it
            actual_sample_size = min(self.sample_size, self.total_lines)

            # Read the first 'actual_sample_size' lines
            reservoir = []
            for _ in range(actual_sample_size):
                line = infile.readline()
                if not line:  # End of file
                    break
                reservoir.append(line)

            # Update actual_sample_size
            actual_sample_size = len(reservoir)

            # Replace elements with gradually decreasing probability
            for i, line in enumerate(infile, start=len(reservoir)):
                j = self.rng.randint(0, i)
                if j < actual_sample_size:
                    reservoir[j] = line

            # Write the sampled lines to the output file
            outfile.writelines(reservoir)

    def index_sample(self):
        # If sample size is larger than total lines, adjust it
        actual_sample_size = min(self.sample_size, self.total_lines)

        # Generate random indices
        indices: Set[int] = set()
        while len(indices) < actual_sample_size:
            indices.add(self.rng.randint(0, self.total_lines - 1))

        # Read the file and write sampled lines
        with open(self.input_file, "r") as infile, open(
            self.output_file, "w"
        ) as outfile:
            for i, line in enumerate(infile):
                if i in indices:
                    outfile.write(line)

    def sample(self, method: str = "reservoir"):
        if method == "reservoir":
            self.reservoir_sample()
        elif method == "index":
            self.index_sample()
        else:
            raise ValueError(
                "Invalid sampling method. Choose 'reservoir' or 'index'."
            )


def main():
    parser = argparse.ArgumentParser(
        description="Sample N random lines from a large text file."
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        required=True,
        help="Number of lines to sample",
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["reservoir", "index"],
        default="reservoir",
        help="Sampling method: 'reservoir' or 'index' (faster)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, help="Seed for random number generator"
    )
    parser.add_argument(
        "-p", "--progress", action="store_true", help="Show progress bar"
    )

    args = parser.parse_args()

    sampler = Sample(
        args.input_file,
        args.output_file,
        args.number,
        progress=args.progress,
        seed=args.seed,
    )
    sampler.sample(method=args.method)


if __name__ == "__main__":
    main()
