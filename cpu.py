"""The CPU"""

class CPU:
    def __init__(self):
        """Constructor for the CPU object."""
        self.ram = [0] * 256  # Simulates 8bit memory that can hold 0-255
        self.reg = [0] * 8    # 8 internal register locations
        self.ir = 0           # Internal register
        self.pc = 0           # Program Counter
        self.mar = 0          # Memory address register
        self.mdr = 0          # Memory data register
        self.fl = 0b00000000  # Flag byte. The last 3 bits contain the LGE flags. 0b00000LGE

        return None

    def load(self, file):
        """Loads a given file into memory."""
        addr = 0
        with open(file, 'r') as f:
            # Get each line
            for line in f:
                try:
                    # If the line is a comment, ignore it
                    if line.startswith('#'):
                        continue
                    else:
                        self.ram[addr] = int(line[:8].strip('\n'), 2)
                    addr += 1
                except:
                    # Empty line, ignore it
                    continue
        return None

    def alu(self, op, reg_a, reg_b):
        """Perform an ALU operation."""
        CMP = 0b10100111
        # The only required operation is the compare operation.
        if op == CMP:
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b10
            else:
                self.fl = 0b1
        return None

    def check_flag(self, flag, n):
        """Checks if a given bit (n) is set.

        Args:
            flag: A byte in the format 00000LGE

        Yields:
            True if the desired bit is 1, else 0.
        """
        return flag & 0b1 << n != 0

    def increment(self, instruction):
        """Get the number of memory spaces to move from the instruction byte.

        Args:
            instruction (byte): The 8 bit instruction

        Yields:
            num: The number of spaces to increment the PC.
        """
        return (instruction >> 6) + 1

    def run(self):
        """Run the program."""
        # Set a ground state
        running = True

        while running:
            # Load the next instruction
            self.ir = self.ram[self.pc]
            # Get the increment number
            n = self.increment(self.ir)

            # HLT
            if self.ir == 0b1:
                # Shut down the program
                running = False

            # LDI
            elif self.ir == 0b10000010:
                # Get addr and data values
                self.mar = self.ram[self.pc + 1]
                self.mdr = self.ram[self.pc + 2]
                # Update the register
                self.ram_write()
                self.pc += n

            # PRN
            elif self.ir == 0b1000111:
                # Print value at register location
                self.mar = self.ram[self.pc + 1]
                self.ram_read()
                print(self.mdr)
                self.pc += n

            # CMP
            elif self.ir == 0b10100111:
                # Get both register values
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                # Set the FL flag by comparing the two values
                self.alu(self.ir, reg_a, reg_b)
                self.pc += n

            # JMP
            elif self.ir == 0b1010100:
                # Jump to given register
                self.pc = self.reg[self.ram[self.pc + 1]]

            # JEQ
            elif self.ir == 0b1010101:
                # Jump to given register if the equal flag is set
                if self.check_flag(self.fl, 0) == True:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += n

            # JNE
            elif self.ir == 0b1010110:
                # Jump to given register if the equal flag is not set
                if self.check_flag(self.fl, 0) == False:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += n

        return None

    def ram_read(self):
        self.mdr = self.reg[self.mar]
        return None
    
    def ram_write(self):
        self.reg[self.mar] = self.mdr
        return None
