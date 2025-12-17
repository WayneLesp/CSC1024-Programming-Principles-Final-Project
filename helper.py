# -------------------------
# File handling helpers
# -------------------------

def read_file(filename):
    """Reads lines from a file, stripping whitespace, and returns a list.
       Returns an empty list if the file does not exist."""
    try:
        with open(filename, "r") as f:
            # Using a list comprehension to read, strip, and filter out empty lines
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def write_file(filename, data_list):
    """Writes all strings in data_list to the file, overwriting existing content."""
    with open(filename, "w") as f:
        for line in data_list:
            f.write(line + "\n")

def append_file(filename, line):
    """Appends a single line to the end of the file."""
    with open(filename, "a") as f:
        f.write(line + "\n")