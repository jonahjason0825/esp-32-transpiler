import os
from lark import Lark, Transformer

grammar = """
    start: statement (_SEP+ statement)* _SEP*
    statement: command_statement | repeat_statement
    command_statement: IDENTIFIER param*
    repeat_statement: "REPEAT" INT "DO" statement+ "END"
    param: INT | STRING | IDENTIFIER
    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
    _SEP: /\\n+/
    %import common.ESCAPED_STRING -> STRING
    %import common.INT
    %ignore /[ \\t]/
"""

class ESPTranspiler(Transformer): 
    # Lookup table mapping DSL actions to ESP-IDF driver macros
    command_map = {
        "setPin": lambda pin_number, pin_state: (
            f"gpio_reset_pin({pin_number}); "
            f"gpio_set_direction({pin_number}, GPIO_MODE_OUTPUT); "
            f"gpio_set_level({pin_number}, {1 if pin_state in ('HIGH', '1') else 0});"
        ),
        "readPin": lambda pin_number: (f"gpio_get_level({pin_number}); "),
        "holdFor": lambda ms: f"vTaskDelay(pdMS_TO_TICKS({ms}));",
        "getTime": lambda: "printf(\"Current time: %ld\\n\", esp_timer_get_time());",
        "blinkBuiltIn": lambda: (
                    f"gpio_reset_pin(12);"
                    f"gpio_set_direction(12, GPIO_MODE_OUTPUT);"
                    f"gpio_set_level(12, 1);"
                ),
        "returnAvailableDRAM": lambda: "printf(\"Available DRAM: %d bytes\\n\", esp_get_free_heap_size());"

    }

    def start(self, items):
        return "\n    ".join(str(item) for item in items)

    def statement(self, items):
        return items[0]

    def param(self, items):
        token = items[0]
        # Return the integer value for INT, string value for others
        return int(token.value) if token.type == 'INT' else token.value

    # Method name matches grammar rule 'command_statement'
    def command_statement(self, items):
        cmd_name = items[0].value
        args = items[1:]
        
        # Access class attribute via self.command_map
        if cmd_name in self.command_map:
            return self.command_map[cmd_name](*args)
        else:
            raise SyntaxError(f"Unknown hardware command: {cmd_name}")

    # Method name matches grammar rule 'repeat_statement'
    def repeat_statement(self, items):
        count = items[0]
        inner_body = "\n        ".join(str(item) for item in items[1:])
        return f"for (int i = 0; i < {count}; i++) {{\n        {inner_body}\n    }}"


parser = Lark(grammar, start='start')

# 1. Read input DSL file
with open("script.easy", "r") as f:
    dsl_code = f.read()

parseTree = parser.parse(dsl_code)
transpiler = ESPTranspiler()
generatedProg = transpiler.transform(parseTree)

# 2. Inject output into C skeleton
with open("template.c", "r") as f:
    template_code = f.read()

outputCode = template_code.replace("//Code_generation_section", generatedProg)

# 3. Save build output to main/main.c
os.makedirs("main", exist_ok=True)
with open("main/main.c", "w") as f:
    f.write(outputCode)

print("Compilation successful. Output written to main/main.c")

