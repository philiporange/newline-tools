import os
import random
import argparse
import tempfile

from .utils import count_lines

from tqdm import tqdm


class Shuffle:
    def __init__(
        self,
        input_file,
        buffer_size=2**30,
        ignore_empty=False,
        progress=False,
        rounds=1,
        seed=None,
    ):
        self.input_file = input_file
        self.buffer_size = buffer_size
        self.file_size = os.path.getsize(input_file)
        self.total_lines = count_lines(input_file)
        self.ignore_empty = ignore_empty
        self.progress = progress
        self.rounds = rounds
        self.seed = seed
        self.rng = random.Random(self.seed)

    def shuffle(self, output_file):
        current_input = self.input_file

        for round in range(self.rounds):
            if self.progress:
                print(f"Starting round {round + 1} of {self.rounds}")

            if round == self.rounds - 1:
                # Last round, write to the final output file
                self._shuffle_once(current_input, output_file)
            else:
                # Intermediate round, write to a temporary file
                with tempfile.NamedTemporaryFile(
                    mode="w+", delete=False
                ) as temp_output:
                    self._shuffle_once(current_input, temp_output.name)
                    if current_input != self.input_file:
                        # Remove the previous temporary file
                        os.remove(current_input)
                    current_input = temp_output.name

    def _shuffle_once(self, input_file, output_file):
        num_temp_files = max((self.file_size // self.buffer_size) + 1, 1)
        temp_files = [
            tempfile.NamedTemporaryFile(mode="w+", delete=False)
            for _ in range(num_temp_files)
        ]
        temp_file_lines = [0] * num_temp_files

        buffer = ""
        temp_file_n = 0

        # Reading and shuffling stage
        with open(input_file, "r") as f:
            read_progress = tqdm(
                total=self.total_lines,
                desc="Reading and shuffling",
                disable=not self.progress,
            )

            for line in f:
                if not line.strip() and self.ignore_empty:
                    continue

                buffer += line
                read_progress.update(1)

                if len(buffer) > self.buffer_size:
                    buffer = buffer.splitlines(True)
                    self.rng.shuffle(buffer)
                    buffer = "".join(buffer)

                    temp_files[temp_file_n].write(buffer)
                    temp_file_lines[temp_file_n] += len(buffer.splitlines())
                    buffer = ""
                    temp_file_n = (temp_file_n + 1) % num_temp_files

            if buffer:
                buffer = buffer.splitlines(True)
                self.rng.shuffle(buffer)
                buffer = "".join(buffer)
                temp_files[temp_file_n].write(buffer)
                temp_file_lines[temp_file_n] += len(buffer.splitlines())

            read_progress.close()

        for temp_file in temp_files:
            temp_file.seek(0)

        # Writing stage
        with open(output_file, "w") as out_file:
            write_progress = tqdm(
                total=self.total_lines,
                desc="Writing shuffled lines",
                disable=not self.progress,
            )

            while temp_files:
                if sum(temp_file_lines) == 0:
                    break

                chosen_index = self.rng.choices(
                    range(len(temp_files)), weights=temp_file_lines, k=1
                )[0]
                temp_f = temp_files[chosen_index]

                line = temp_f.readline()
                if not line:
                    temp_f.close()
                    temp_files.pop(chosen_index)
                    temp_file_lines.pop(chosen_index)
                else:
                    if line[-1] != "\n":
                        line += "\n"
                    out_file.write(line)
                    temp_file_lines[chosen_index] -= 1
                    write_progress.update(1)

            write_progress.close()

        # Cleanup stage
        cleanup_progress = tqdm(
            total=num_temp_files,
            desc="Cleaning up temp files",
            disable=not self.progress,
        )
        for temp_file in temp_files:
            os.remove(temp_file.name)
            cleanup_progress.update(1)
        cleanup_progress.close()


def main():
    parser = argparse.ArgumentParser(description="Shuffle a large text file.")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument(
        "-b",
        "--buffer_size",
        type=int,
        default=2**30,
        help="Buffer size in bytes (default: 1GB)",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bars during shuffling",
    )
    parser.add_argument(
        "--include_empty",
        action="store_true",
        help="Ignore empty lines during shuffling",
    )
    parser.add_argument(
        "-r",
        "--rounds",
        type=int,
        default=1,
        help="Number of shuffling rounds (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed for random number generator (for reproducibility)",
    )

    args = parser.parse_args()

    args.buffer_size = max(
        args.buffer_size, 2**20
    )  # Minimum buffer size of 1MB

    shuffler = Shuffle(
        args.input_file,
        buffer_size=args.buffer_size,
        progress=args.progress,
        ignore_empty=not args.include_empty,
        rounds=args.rounds,
        seed=args.seed,
    )
    shuffler.shuffle(args.output_file)


if __name__ == "__main__":
    main()
