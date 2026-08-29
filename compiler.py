import os
from lark import Lark, Transformer, v_args
grammar = """
    start: command+
    command: "setPin" INT STATE
    STATE: "HIGH" | "LOW"
    %import common.WS
    %import common.INT
    %ignore WS
"""
#now creates an array items. items[0] stores the pin number and items[1] 
# stores the state of the pin 
#if items[1] is HIGH then the pin is set to HIGH and if items[1] is LOW 
# then the pin is set to LOW
class ESPTranspiler(Transformer): 
    def command (self, items):
        pin_number = int(items[0])
        state = 1 if items[1] == "HIGH" else 0
        return f"gpio_set_direction({pin_number}, OUTPUT);gpio_set_level({pin_number}, {state});"
    def start (self, items): #combines all the individual C statements produced by command rules 
    #into a single, cleanly formatted text block.
        return "\n    ".join(items)

parser=Lark(grammar, start='start')
#read the input DSL (domain specific language) file 
with open("script.easy", "r") as f:
    dsl_code = f.read()
parseTree=parser.parse(dsl_code)
transpiler=ESPTranspiler()
generatedProg=transpiler.transform(parseTree)

with open ("template.c", "r") as f:
    template_code = f.read()
outputCode=template_code.replace("//Code_generation_section", generatedProg)
#now save to the correct branch: main/main.c
os.makedirs("main", exist_ok=True)
with open("main/main.c", "w") as f:
    f.write(outputCode)

print("Compilation successful. Output written to main/main.c")

