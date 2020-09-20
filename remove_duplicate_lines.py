#!/usr/bin/env python

import sys
import os

def main() -> int:
    num_args = len(sys.argv)
    if num_args < 2:
        print("Usage: ./remove_duplicate_lines.py <filename>")
        return 1

    filename = sys.argv[1]
    ignore_lines = sys.argv[2:]
    for i in range(0, len(ignore_lines)):
        ignore_lines[i] += "\n"
    ignore_lines.append("\n")

    seen_lines = {}

    temp_file = open("./duplicates.tmp", "w+")
    try:
        with open(filename, "r") as file:
            for line in file.readlines():
                override = line in ignore_lines
                if not (line in seen_lines) or override:
                    temp_file.write(line)
                    if not override:
                        seen_lines[line] = True
    except Exception as e:
        print(f"Error: {e}")

    #os.rename("./duplicates.tmp", filename)

if __name__ == "__main__":
    sys.exit(main())
