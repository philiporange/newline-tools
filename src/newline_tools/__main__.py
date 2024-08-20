#!/usr/bin/env python3

import argparse
import sys

from . import Shuffle, Dedupe, Split, Sample


def main():
    parser = argparse.ArgumentParser(
        description="Newline Tools - Operations on large text files"
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # Shuffle command
    shuffle_parser = subparsers.add_parser(
        "shuffle", help="Shuffle lines in a file"
    )
    shuffle_parser.add_argument("input_file", help="Path to the input file")
    shuffle_parser.add_argument("output_file", help="Path to the output file")
    shuffle_parser.add_argument(
        "-b",
        "--buffer_size",
        type=int,
        default=2**30,
        help="Buffer size in bytes (default: 1GB)",
    )
    shuffle_parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar during shuffling",
    )
    shuffle_parser.add_argument(
        "--seed",
        type=int,
        help="Seed for random number generator (for reproducibility)",
    )

    # Dedupe command
    dedupe_parser = subparsers.add_parser(
        "dedupe", help="Remove duplicate lines from a file"
    )
    dedupe_parser.add_argument("input_file", help="Path to the input file")
    dedupe_parser.add_argument("output_file", help="Path to the output file")
    dedupe_parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar during deduplication",
    )
    dedupe_parser.add_argument(
        "--error_ratio",
        type=float,
        default=1e-5,
        help="Error ratio for the Bloom filter (default: 1e-5)",
    )

    # Split command
    split_parser = subparsers.add_parser(
        "split", help="Split a file into multiple parts"
    )
    split_parser.add_argument("input_file", help="Path to the input file")
    split_parser.add_argument("output_prefix", help="Prefix for output files")
    split_parser.add_argument(
        "-n", "--num_parts", type=int, help="Number of parts to split into"
    )
    split_parser.add_argument(
        "-s",
        "--size",
        type=str,
        help="Size of each part (e.g., '100MB', '1GB')",
    )
    split_parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar during splitting",
    )

    # Sample command
    sample_parser = subparsers.add_parser(
        "sample", help="Sample lines from a file"
    )
    sample_parser.add_argument("input_file", help="Path to the input file")
    sample_parser.add_argument("output_file", help="Path to the output file")
    sample_parser.add_argument(
        "-n", "--num_lines", type=int, help="Number of lines to sample"
    )
    sample_parser.add_argument(
        "-p", "--percentage", type=float, help="Percentage of lines to sample"
    )
    sample_parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar during sampling",
    )
    sample_parser.add_argument(
        "--seed",
        type=int,
        help="Seed for random number generator (for reproducibility)",
    )

    args = parser.parse_args()

    if args.command == "shuffle":
        shuffler = Shuffle(
            args.input_file,
            buffer_size=args.buffer_size,
            progress=args.progress,
            seed=args.seed,
        )
        shuffler.shuffle(args.output_file)

    elif args.command == "dedupe":
        deduper = Dedupe(
            args.input_file,
            progress=args.progress,
        )
        deduper.dedupe(args.output_file, error_ratio=args.error_ratio)

    elif args.command == "split":
        splitter = Split(
            args.input_file,
            output_prefix=args.output_prefix,
            progress=args.progress,
        )
        if args.num_parts:
            splitter.split_by_parts(args.num_parts)
        elif args.size:
            splitter.split_by_size(args.size)
        else:
            print("Error: Either --num_parts or --size must be specified")
            sys.exit(1)

    elif args.command == "sample":
        if args.num_lines:
            sample_size = args.num_lines
        elif args.percentage:
            # Calculate the number of lines based on the percentage
            total_lines = sum(1 for _ in open(args.input_file))
            sample_size = int(total_lines * args.percentage / 100)
        else:
            print(
                "Error: Either --num_lines or --percentage must be specified"
            )
            sys.exit(1)

        sampler = Sample(
            args.input_file,
            args.output_file,
            sample_size,
            progress=args.progress,
            seed=args.seed,
        )
        sampler.sample()

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
