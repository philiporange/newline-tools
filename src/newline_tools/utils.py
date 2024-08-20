def count_lines(input_file: str) -> int:
    with open(input_file, "rb") as f:
        return sum(1 for _ in f)
