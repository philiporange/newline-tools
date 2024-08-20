import unittest
import os
import tempfile

from src.newline_tools.dedupe import Dedupe


class TestDedupe(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

        # Create a test input file with duplicate lines
        self.input_file = os.path.join(self.temp_dir, "input.txt")
        with open(self.input_file, "w") as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 1\n")  # Duplicate
            f.write("Line 3\n")
            f.write("Line 2\n")  # Duplicate
            f.write("Line 4\n")

        self.output_file = os.path.join(self.temp_dir, "output.txt")

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_dedupe(self):
        deduper = Dedupe(self.input_file)
        deduper.dedupe(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if duplicates were removed
        with open(self.output_file, "r") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 4)  # Should be 4 unique lines
        self.assertEqual(
            lines, ["Line 1\n", "Line 2\n", "Line 3\n", "Line 4\n"]
        )

    def test_dedupe_empty_file(self):
        empty_file = os.path.join(self.temp_dir, "empty.txt")
        open(empty_file, "w").close()  # Create an empty file

        deduper = Dedupe(empty_file)
        deduper.dedupe(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if output file is empty
        with open(self.output_file, "r") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 0)

    def test_dedupe_no_duplicates(self):
        no_dupes_file = os.path.join(self.temp_dir, "no_dupes.txt")
        with open(no_dupes_file, "w") as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 3\n")

        deduper = Dedupe(no_dupes_file)
        deduper.dedupe(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if all lines are preserved
        with open(self.output_file, "r") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 3)
        self.assertEqual(lines, ["Line 1\n", "Line 2\n", "Line 3\n"])

    def test_dedupe_all_duplicates(self):
        all_dupes_file = os.path.join(self.temp_dir, "all_dupes.txt")
        with open(all_dupes_file, "w") as f:
            f.write("Line 1\n" * 5)

        deduper = Dedupe(all_dupes_file)
        deduper.dedupe(self.output_file)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if only one line remains
        with open(self.output_file, "r") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 1)
        self.assertEqual(lines, ["Line 1\n"])


if __name__ == "__main__":
    unittest.main()
