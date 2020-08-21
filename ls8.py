"""Run a given ls8 program from .ls8 ext"""

import sys
from cpu import CPU

cpu = CPU()

# Get the file name
file = sys.argv[1]

if __name__ == "__main__":
    # Load the program into memory
    cpu.load(file)
    # Run it
    cpu.run()
