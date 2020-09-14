"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = False
        self.flag = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xf4

    def load(self):
        """Load a program into memory."""

        self.read_args()

    def read_args(self):
        params = sys.argv

        if len(params) != 2:
            print(f"Usage file.py filename")
            sys.exit(1)

        if len(params) == 2:
            try:
                with open(params[1]) as f:
                    address = 0
                    for line in f:
                        split = line.split("#")
                        num = split[0].strip()

                        if num == '':
                            continue
                        num2 = int("0b"+num, 2)

                        self.ram_write(address, num2)
                        address += 1

            except:
                print("File not found")
                sys.exit(2)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3

        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag[-3] = 1

            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag[-2] = 1

            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag[-1] = 1
            self.pc += 3

        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
            self.pc += 3

        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
            self.pc += 3

        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
            self.pc += 3

        elif op == "NOT":
            self.reg[reg_a] = ~ self.reg[reg_a]
            self.pc += 2

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        HLT = 0b00000001
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        AND = 0b10101000
        OR = 0b10101010
        XOR = 0b10101011
        NOT = 0b01101001

        self.load()
        self.trace()

        while self.running:
            instruction = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            if instruction == LDI:
                self.reg[op_a] = op_b
                self.pc += 3

            elif instruction == PRN:
                print(self.reg[op_a])
                self.pc += 2

            elif instruction == MUL:
                self.alu("MUL", op_a, op_b)

            elif instruction == HLT:
                self.running = False

            elif instruction == PUSH:
                self.reg[self.sp] -= 1
                op_a = self.ram_read(self.pc + 1)

                reg_val = self.reg[op_a]
                self.ram_write(self.reg[self.sp], reg_val)
                self.pc += 2

            elif instruction == POP:
                op_a = self.ram_read(self.pc + 1)
                popped_val = self.ram_read(self.reg[self.sp])
                self.reg[op_a] = popped_val
                self.reg[self.sp] += 1
                self.pc += 2

            elif instruction == ADD:
                self.alu("ADD", op_a, op_b)

            elif instruction == CALL:
                address = self.pc + 2
                self.reg[self.sp] -= 1
                self.ram_write(self.reg[self.sp], address)
                self.pc = self.reg[op_a]

            elif instruction == RET:
                self.pc = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1

            elif instruction == CMP:
                self.alu("CMP", op_a, op_b)

            elif instruction == JMP:
                self.pc = self.reg[op_a]

            elif instruction == JEQ:
                if self.flag[-1] == 1:
                    self.pc = self.reg[op_a]
                else:
                    self.pc += 2

            elif instruction == JNE:
                if self.flag[-1] == 0:
                    self.pc = self.reg[op_a]
                else:
                    self.pc += 2

            elif instruction == AND:
                self.alu("AND", op_a, op_b)

            elif instruction == OR:
                self.alu("OR", op_a, op_b)

            elif instruction == XOR:
                self.alu("XOR", op_a, op_b)

            elif instruction == NOT:
                self.alu("NOT", op_a, op_b)


cpu = CPU()

cpu.run()
