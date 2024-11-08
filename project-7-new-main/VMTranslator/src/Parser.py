import re
from CommandType import CommandType

class Parser:
    def __init__(self, input_file):
        self.pointer = -1
        self.current_command = []
        self.instructions = []
        self.populate_instructions(input_file)

    def has_more_commands(self):
        return self.pointer < len(self.instructions) - 1

    def advance(self):
        self.pointer += 1
        self.current_command = self.instructions[self.pointer].split()

    def command_type(self):
        type_ = self.current_command[0].lower()
        command_map = {
            "add": CommandType.C_ARITHMETIC,
            "sub": CommandType.C_ARITHMETIC,
            "neg": CommandType.C_ARITHMETIC,
            "eq": CommandType.C_ARITHMETIC,
            "gt": CommandType.C_ARITHMETIC,
            "lt": CommandType.C_ARITHMETIC,
            "and": CommandType.C_ARITHMETIC,
            "or": CommandType.C_ARITHMETIC,
            "not": CommandType.C_ARITHMETIC,
            "push": CommandType.C_PUSH,
            "pop": CommandType.C_POP,
            "label": CommandType.C_LABEL,
            "goto": CommandType.C_GOTO,
            "if-goto": CommandType.C_IF,
            "function": CommandType.C_FUNCTION,
            "call": CommandType.C_CALL,
            "return": CommandType.C_RETURN,
        }
        if type_ in command_map:
            return command_map[type_]
        else:
            raise ValueError(f"Invalid command type: {type_}")

    def arg1(self):
        if self.command_type() == CommandType.C_ARITHMETIC:
            return self.current_command[0]
        else:
            return self.current_command[1]

    def arg2(self):
        try:
            return int(self.current_command[2])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid argument: {e}")

    def populate_instructions(self, input_file):
        try:
            with open(input_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("//"):
                        continue  # Skip empty lines and whole-line comments
                    command = ""
                    for token in line.split():
                        if token.startswith("//"):
                            break  # Skip inline comments
                        command += token + " "
                    if command.strip():
                        self.instructions.append(command.strip())
        except FileNotFoundError as fnf:
            raise FileNotFoundError(f"File not found: {fnf}")
