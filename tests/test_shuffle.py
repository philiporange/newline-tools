import unittest
import os
import tempfile
from collections import Counter

from src.newline_tools.shuffle import Shuffle

from scipy import stats


class TestShuffle(unittest.TestCase):
    N = 500000

    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

        # Create a test input file
        self.input_file = os.path.join(self.temp_dir, "input.txt")
        with open(self.input_file, "w") as f:
            for i in range(self.N):
                f.write(f"Line {i}\n")

        self.output_file = os.path.join(self.temp_dir, "output.txt")

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_shuffle(self):
        shuffler = Shuffle(self.input_file, buffer_size=2**20)
        shuffler.shuffle(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if the number of lines in output file matches input file
        with open(self.output_file, "r") as f:
            output_lines = f.readlines()
        self.assertEqual(len(output_lines), self.N)

        # Check if lines are shuffled (not in the same order as input)
        with open(self.input_file, "r") as f:
            input_lines = f.readlines()
        self.assertNotEqual(input_lines, output_lines)

        # Check if all original lines are present in the output
        input_set = set(input_lines)
        output_set = set(output_lines)
        self.assertEqual(input_set, output_set)

    def test_empty_file(self):
        # Create an empty input file
        empty_file = os.path.join(self.temp_dir, "empty.txt")
        open(empty_file, "w").close()

        shuffler = Shuffle(empty_file)
        shuffler.shuffle(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if output file is empty
        with open(self.output_file, "r") as f:
            output_lines = f.readlines()
        self.assertEqual(len(output_lines), 0)

    def test_single_line_file(self):
        # Create a file with a single line
        single_line_file = os.path.join(self.temp_dir, "single_line.txt")
        with open(single_line_file, "w") as f:
            f.write("Single line\n")

        shuffler = Shuffle(single_line_file)
        shuffler.shuffle(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if output file contains the single line
        with open(self.output_file, "r") as f:
            output_lines = f.readlines()
        self.assertEqual(len(output_lines), 1)
        self.assertEqual(output_lines[0], "Single line\n")

    def test_large_buffer(self):
        shuffler = Shuffle(self.input_file, buffer_size=2**30)
        shuffler.shuffle(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if the number of lines in output file matches input file
        with open(self.output_file, "r") as f:
            output_lines = f.readlines()
        self.assertEqual(len(output_lines), self.N)

    def test_mixing(self):
        N = self.N
        num_parts = 10

        # Create original list
        original = list(range(N))

        # Shuffle
        shuffler = Shuffle(self.input_file, buffer_size=2**20)
        shuffler.shuffle(self.output_file)

        # Read shuffled list
        with open(self.output_file, "r") as f:
            shuffled = [int(line.strip().split()[1]) for line in f]

        # Divide into parts
        part_size = N // num_parts
        parts = [
            shuffled[i * part_size : (i + 1) * part_size]
            for i in range(num_parts)
        ]

        # Count occurrences of each number in each part
        counts = [Counter(part) for part in parts]

        # Perform Kolmogorov-Smirnov test
        original_positions = {num: i / N for i, num in enumerate(original)}
        shuffled_positions = {num: i / N for i, num in enumerate(shuffled)}

        ks_statistic, p_value = stats.ks_2samp(
            list(original_positions.values()),
            list(shuffled_positions.values()),
        )

        # Check if p-value is greater than significance level (e.g., 0.05)
        self.assertGreater(
            p_value,
            0.05,
            f"Kolmogorov-Smirnov test failed with p-value {p_value}",
        )

        # Additional test: check if numbers are evenly distributed across parts
        for num in range(N):
            num_counts = [count[num] for count in counts]
            chi2_statistic, chi2_p_value = stats.chisquare(num_counts)
            self.assertGreater(
                chi2_p_value,
                0.05 / N,  # Bonferroni correction
                f"Chi-square test failed for number {num} with p-value {chi2_p_value}",
            )


if __name__ == "__main__":
    unittest.main()
