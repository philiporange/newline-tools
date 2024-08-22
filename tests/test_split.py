import unittest
import os
import tempfile

from src.newline_tools.split import Split


class TestSplit(unittest.TestCase):
    def setUp(self):
        # Create a temporary file with some test content
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, "input.txt")
        with open(self.input_file, "w") as f:
            f.write("\n".join(f"Line {i}" for i in range(1, 101)))  # 100 lines

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_split_by_number(self):
        splitter = Split(self.input_file)
        splitter.split_by_parts(5)  # Split into 5 files

        # Check if 5 files were created
        output_files = [
            f for f in os.listdir(self.temp_dir) if f.startswith("input-")
        ]
        self.assertEqual(len(output_files), 5)

        # Check if each file has 20 lines (100 / 5 = 20)
        for file in output_files:
            with open(os.path.join(self.temp_dir, file), "r") as f:
                self.assertEqual(len(f.readlines()), 20)

    def test_split_by_size(self):
        splitter = Split(self.input_file)
        splitter.split_by_size(30)  # Split into files of 30 lines each

        # Check if 4 files were created (100 lines / 30 lines per file = 3.33, rounded up to 4)
        output_files = [
            f for f in os.listdir(self.temp_dir) if f.startswith("input-")
        ]
        self.assertEqual(len(output_files), 4)

        # Check if the first 3 files have 30 lines and the last one has 10 lines
        for i, file in enumerate(sorted(output_files)):
            with open(os.path.join(self.temp_dir, file), "r") as f:
                if i < 3:
                    self.assertEqual(len(f.readlines()), 30)
                else:
                    self.assertEqual(len(f.readlines()), 10)

    def test_custom_output_prefix(self):
        custom_prefix = os.path.join(self.temp_dir, "custom_output")
        splitter = Split(self.input_file, custom_prefix)
        splitter.split_by_parts(2)

        # Check if files with custom prefix were created
        output_files = [
            f
            for f in os.listdir(self.temp_dir)
            if f.startswith("custom_output-")
        ]
        self.assertEqual(len(output_files), 2)

    def test_empty_input_file(self):
        # Create an empty input file
        empty_file = os.path.join(self.temp_dir, "empty.txt")
        open(empty_file, "w").close()

        splitter = Split(empty_file)
        splitter.split_by_parts(5)

        # Check if no output files were created
        output_files = [
            f for f in os.listdir(self.temp_dir) if f.startswith("empty-")
        ]
        self.assertEqual(len(output_files), 0)

    def test_split_by_proportion(self):
        splitter = Split(self.input_file)
        proportions = [0.3, 0.5, 0.2]
        splitter.split_by_proportion(proportions)

        # Check if 3 files were created
        output_files = [
            f for f in os.listdir(self.temp_dir) if f.startswith("input-")
        ]
        self.assertEqual(len(output_files), 3)

        # Check if each file has the correct number of lines
        expected_lines = [30, 50, 20]
        for i, file in enumerate(sorted(output_files)):
            with open(os.path.join(self.temp_dir, file), "r") as f:
                self.assertEqual(len(f.readlines()), expected_lines[i])


if __name__ == "__main__":
    unittest.main()
