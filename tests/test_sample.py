import unittest
import os
import tempfile
from src.newline_tools.sample import Sample


class TestSample(unittest.TestCase):
    def setUp(self):
        # Create a temporary file with some test content
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, "input.txt")
        with open(self.input_file, "w") as f:
            f.write("\n".join(f"Line {i}" for i in range(1, 101)))  # 100 lines

        self.output_file = os.path.join(self.temp_dir, "output.txt")

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_reservoir_sample(self):
        sample_size = 20
        sampler = Sample(self.input_file, self.output_file, sample_size)
        sampler.sample(method="reservoir")

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if the correct number of lines were sampled
        with open(self.output_file, "r") as f:
            sampled_lines = f.readlines()
        self.assertEqual(len(sampled_lines), sample_size)

        # Check if all sampled lines are unique
        self.assertEqual(len(set(sampled_lines)), sample_size)

    def test_index_sample(self):
        sample_size = 30
        sampler = Sample(self.input_file, self.output_file, sample_size)
        sampler.sample(method="index")

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if the correct number of lines were sampled
        with open(self.output_file, "r") as f:
            sampled_lines = f.readlines()
        self.assertEqual(len(sampled_lines), sample_size)

        # Check if all sampled lines are unique
        self.assertEqual(len(set(sampled_lines)), sample_size)

    def test_sample_size_larger_than_input(self):
        sample_size = 150  # Larger than the input file (100 lines)
        sampler = Sample(self.input_file, self.output_file, sample_size)
        sampler.sample()

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Check if the number of sampled lines equals the input file size
        with open(self.output_file, "r") as f:
            sampled_lines = f.readlines()
        self.assertEqual(len(sampled_lines), 100)  # Should be 100, not 150

    def test_invalid_sampling_method(self):
        sample_size = 10
        sampler = Sample(self.input_file, self.output_file, sample_size)

        with self.assertRaises(ValueError):
            sampler.sample(method="invalid_method")


if __name__ == "__main__":
    unittest.main()
