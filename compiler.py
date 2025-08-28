import re as regex
import time
import struct

start_time: float = time.perf_counter()

i=0


regs: list[int] = [
            0,#"rax" 0
            0,#"rbx" 1
            0,#"rcx" 2
            0,#"rsp" 3
            0,#"rbp" 4
            0,#"r0"  5
            0,#"r1"  6
            0,#"r2"  7
            0,#"r3"  8
            0,#"r4"  9
            0,#"r5"  10
            0,#"r6"  11
            0 #"r7"  12
            ]



def eval_address(expr: str) -> int:
    """
    Evaluate x86-style address expressions:
    - [rax]
    - [rbp-8]
    - [rax+rbx*2+16]
    - [rbx*4+32]
    """
    

    # Safe eval
    return eval(expr)

sizes: dict[str, int] = {"byte":0,"word":1,"dword":2,"qword":3}
reg_look: dict[str, int]={
"rax": 0,
"rbx": 1,
"rcx": 2,
"rsp": 3,
"rbp": 4,
"r0" : 5,
"r1" : 6,
"r2" : 7,
"r3" : 8,
"r4" : 9,
"r5" : 10,
"r6" : 11,
"r7" : 12}

op_look: dict[str, int]={"mov":0,
                         "inc": 1,
                         "dec": 2,
                         "neg": 3,  
                         "shl": 4,  
                         "shr": 5,  
                         "add": 6,  
                         "sub": 7,  
                         "mul": 8,  
                         "div": 9,
                         "cmp": 10,
                         "jmp": 11,
                         "jne": 12,
                         "je":  13,
                         "jg":  14,
                         "jl":  15,
                         "pri": 16
                            }


        
            
comands: list[str] =["mov","add","sub","mul","div","cmp","jmp","jne","jeq","lea","pri"] #pri is definitly asm yeah


lables :dict[str,int]= {}

addr_funcs:dict[str,int]={}

def cmem_lab():
    ina=0
    while True:
        yield ina
        ina+=1

mem_lab = cmem_lab()


with open("input.asm","r") as file:
    text: list[str]=file.readlines()

with open("mem.h","w") as hfile:
    hfile.write("extern int64_t regs[];\n")
    hfile.write("typedef size_t (*mem_func_t)();\n")
    hfile.write("\n")

    



def form_mem(expr) -> int:
    if expr in addr_funcs:
        return addr_funcs[expr]
    
    func_num: int = next(mem_lab)

    addr_funcs[expr] = func_num

    with open("mem.h","a") as hdfile:
        hdfile.write(f"static inline size_t mem_{func_num}() {{ return {expr}; }}\n")

    return func_num
    

    

    




def parse_line(line:str ):
    lin: list[str] = line.replace(",", " ").split()
    nlin = []
    i=0
    while i  < len(lin):
        if lin[i].isnumeric():
            nlin.append((0, int(lin[i])))
            i+=1
        elif lin[i] in reg_look:
            nlin.append((1,reg_look[lin[i]]))
            i+=1
        elif lin[i] in sizes.keys() and i < (len(lin)-2):
            
            size: int=sizes[lin[i]]
            
            expr: str = lin[i+2][1:-1]

            expr = expr.replace(" ", "")
            texpr = str(expr)

            # Replace registers with their numeric values
            for reg in reg_look.keys():
                texpr = texpr.replace(reg, str(regs[reg_look[reg]]))

            # Validate: only numbers, + - * allowed now
            if not regex.fullmatch(r"[0-9+\-*()]+", texpr):
                raise SyntaxError(f"Invalid memory expression: {texpr}")

            # Replace registers with their acces
            for reg in reg_look:
                expr = expr.replace(reg, f"regs[{reg_look[reg]}]")

            fnum: int=form_mem(expr)

            val: int = (size << 30) | fnum

            nlin.append((2, val))
            
            i+=3
        elif lin[i].startswith(";"):
            return nlin
        elif lin[i] in op_look:
            nlin.append(op_look[lin[i]])
            i+=1
        elif lin[i]:
            
            nlin.append(lin[i])
            i+=1

        else:
            i+=1

    return nlin




ocode:list[str] = []

for line in text:
    laa: list[str]=parse_line(line)
    #print(laa)
    if laa:
        ocode.append(laa)  # type: ignore


# Pass 1: collect labels

code = []
labels = {}

#kp

for line in ocode:
    # If it's a label, map it to the current instruction index
    if isinstance(line[0], str) and line[0].endswith(":"):
        label = line[0]
        if label in labels:
            raise SyntaxError(f"Duplicate label: {label}")
        labels[label] = len(code)   # points to *next* instruction index
    else:
        code.append(line)

        


# Pass 2: replace lables by int

for instr in code:
    for j in range(1, len(instr)):   # look at operands
        if isinstance(instr[j], str) and instr[j] in labels:
            instr[j] = (0, labels[instr[j]])

    

        


# Pass 3: execution loop

print(code)



def encode_program(ccode):
    blob = bytearray()
    for instr in ccode:
        opcode = instr[0]
        operands:list[tuple] = instr[1:]

        for i in range(2-len(operands)):
            operands.append((0xbc,0xABABABAB))
        #print(operands)
        blob.append(opcode)
        for mode, val in operands:
            blob.append(mode)
            blob.extend(struct.pack("<I", val))  # 4-byte little-endian
    return bytes(blob)

# Example
program = [[0, (1,0)], [0]]
binary = encode_program(code)

with open("program.bin", "wb") as f:
    f.write(binary)

with open("mem.h", "a") as fc:
    fc.write("\nstatic mem_func_t mem_table[] = {")

    
    for num in addr_funcs.values():
        fc.write(f"mem_{num},")

    fc.write("};")
    







    


end_time: float = time.perf_counter()
print(f"compile time: {end_time - start_time:.6f} seconds")