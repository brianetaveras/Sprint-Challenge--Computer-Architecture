import sys


class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.running = False
        self.commands = {
            "PRN": 0b01000111,
            "CAL": 0b01010000,
            "HLT": 0b00000001,
            "CMP": 0b10100111,
            "LDI": 0b10000010,
            "MUL": 0b10100010,
            "JNE": 0b01010110,
            "PSH": 0b01000101,
            "POP": 0b01000110,
            "RET": 0b00010001,
            "JMP": 0b01010100,
            "JEQ": 0b01010101,
        }
        self.fl = {
            "E": 0,  # Equal
            "L": 0,  # Less than
            "G": 0,  # Greater than
        }
    def load(self):
        address = 0
        program = []

        if len(sys.argv) != 2:
            print("Filename is required")
            sys.exit(1)

        tmp = []
        with open(sys.argv[1], 'r') as file:
            tmp = file.readlines()

            for i in tmp:
                line_split = i.split()

                if not len(line_split) or line_split[0] == "#":
                    continue

                program.append(int(line_split[0], 2))

            for action in program:
                self.ram[address] = action
                address += 1
    def ram_read(self, location):
        return self.ram[location]

    def ram_write(self, location, value):
        self.ram[location] = value
        return self.ram[location]

    def alu(self, operation, reg_a, reg_b):
        if operation == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif operation == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif operation == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif operation == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif operation == "CMP":
            if reg_a == reg_b:
                self.fl["E"] = 1
            elif reg_a < reg_b:
                self.fl["L"] = 1
            elif reg_a > reg_b:
                self.fl["G"] = 1

        else:
            raise Exception("Unsopported ALU operation")

    def run(self):
        self.running = True
        self.reg[self.sp] = len(self.ram)

        while self.running:

            action =  self.ram_read(self.pc)

            if action == self.commands["LDI"]:
                register_number = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[register_number] = value
                self.pc += 3
            elif action == self.commands["PRN"]:
                register_number = self.ram_read(self.pc + 1)
                print(self.reg[register_number])
                self.pc += 2  
            elif action == self.commands["MUL"]:
                reg_a = self.ram_read(self.pc + 1)  
                reg_b = self.ram_read(self.pc + 2) 
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3 
            elif action == self.commands["PSH"]:
                given_register = self.ram_read(self.pc + 1)
                value_in_register = self.reg[given_register]
                self.reg[self.sp] -= 1
                self.ram_write(value_in_register,
                self.ram_read(self.reg[self.sp]))
                self.pc += 2
            elif action == self.commands["POP"]:
                given_register = self.ram_read(self.pc + 1)
                self.ram_write(
                    given_register, self.ram_read(self.reg[self.sp]))
                self.reg[self.sp] += 1
                self.pc += 2

            elif action == self.commands["CAL"]:
                print('register at pc', self.reg[self.pc])
                given_register = self.ram_read(self.pc + 1)
                self.reg[self.sp] -= 1
                self.ram_write(self.ram[self.pc], self.pc + 2)
                self.pc = self.reg[given_register]

            elif action == self.commands["RET"]:
                self.pc = self.ram_read(self.reg[self.pc])
                self.reg[self.pc] += 1

            elif action == self.commands["CMP"]:
                reg_a = self.reg[self.ram_read(self.pc + 1)]
                reg_b = self.reg[self.ram_read(self.pc + 2)]
                self.alu("CMP", reg_a, reg_b)
                self.pc += 3


            elif action == self.commands["JMP"]:  
                given_register = self.ram_read(self.pc + 1)
                self.pc = self.reg[given_register]

            elif action == self.commands["JEQ"]:  
                if self.fl["E"]:
                    given_register = self.ram_read(self.pc + 1)
                    self.pc = self.reg[given_register]
                else:
                    self.pc += 2

            elif action == self.commands["JNE"]: 
                if not self.fl["E"]:
                    given_register = self.ram_read(self.pc + 1)
                    self.pc = self.reg[given_register]
                else:
                    self.pc += 2

            elif action == self.commands["HLT"]:  
                self.running = False
                self.pc += 1

            else:
                print(f'Unknown action: {(action)}')
                self.pc += 1
            




cpu = CPU()
cpu.load()
cpu.run()