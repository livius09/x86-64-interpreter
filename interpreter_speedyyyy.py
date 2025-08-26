import re as regex
import time

i=0

class ccpu:
    def __init__(self) -> None:
        
        self.regs: list[int] = [
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


        # instantiate the ALU as part of the CPU
        self.alu = self.calu()
        self.mem = self.cmem()

    class cmem:
        def __init__(self) -> None:
            self.MEMORY_SIZE = 16 * 1024  # 64 KB
            self.memory = bytearray(self.MEMORY_SIZE)

        def read_mem(self,adr:int,size:int) -> int:
            return int.from_bytes(self.memory[adr:adr+size], "little")
        
        def write_mem(self,val:int,adr:int,size:int) -> None:
            self.memory[adr:adr+size] = val.to_bytes(size, "little")

    class calu:
        def __init__(self) -> None:
            self.flags: dict[str, bool] = {
                "zf": False,  # zero flag
                "gf": False,  # greater flag
                "lf": False,  # less flag
                "cf": False,  # carry flag (placeholder)
            }
            self.branch = self.cbranch(self)

        def inc(self, a:str) -> None:
            write_val(a,get_val(a)+1)

        def dec(self, a:str) -> None:
            write_val(a,get_val(a)-1)

        def neg(self, a:str) -> None:
            write_val(a,get_val(a)*-1)

        def add(self, a:str, b:str) -> None:
            result: int = get_val(a) + get_val(b)
            self.set_flags(result)
            write_val(a,result)

        def sub(self, a:str, b:str) -> None:
            result: int = get_val(a) - get_val(b)
            self.set_flags(result)
            write_val(a,result)

        def mul(self, a:str, b:str) -> None:
            result: int = get_val(a) * get_val(b)
            self.set_flags(result)
            write_val(a,result)

        def div(self, a:str, b:str) -> None:
            result: int = get_val(a) // get_val(b)
            self.set_flags(result)
            write_val(a,result)

        def shl(self, a:str, b:str) -> None:
            write_val(a,get_val(a) << get_val(b))

        def shr(self, a:str, b:str) -> None:
            write_val(a,get_val(a) >> get_val(b))

        
        def set_flags(self,a:int) -> None:
            self.flags["zf"] = (a == 0)
            self.flags["sf"] = (a < 0)  


        def test(self, a, b) -> None:
            self.set_flags(a&b)

        def cmp(self, a, b) -> None:
            self.set_flags(get_val(a)-get_val(b))

        class cbranch:
            def __init__(self, alu) -> None:
                self.alu = alu   # keep reference to ALU

            def jmp(self, a) -> None:
                global i
                i = a[1]

            def jne(self, a) -> None:
                if not self.alu.flags["zf"]:   
                    global i
                    i = a[1]

            def je(self, a) -> None:
                if self.alu.flags["zf"]:   
                    global i
                    i = a[1]

            def jge(self, a) -> None:
                if not self.alu.flags["gf"]:
                    global i
                    i = a[1]
                    





cpu=ccpu()


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

sizes: dict[str, int] = {"byte":1,"word":2,"dword":4,"qword":8}
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
                         "neg": 2,  
                         "shl": 3,  
                         "shr": 4,  
                         "add": 5,  
                         "sub": 6,  
                         "mul": 7,  
                         "div": 8,  
                         "cmp": 9,
                         "jmp": 10,
                         "jne": 11,
                         "je": 12,
                         "jmg": 13,
                         "pri": 14,
                            }

    
def get_val(op) -> int:
    match op[0]:
        case 0:
            return op[1]
        case 1:
            return cpu.regs[op[1]]
        case 2:
            return cpu.mem.read_mem(op[2](), op[1])
        case _:
            raise SyntaxError("balls")

    

def write_val(op,val:int) -> None:
    if op[0]==1:
        cpu.regs[op[1]] = val

    elif op[0]==2:
        cpu.mem.write_mem(val,get_val(op[2]),op[1])

    else:
        raise SyntaxError("ligma")


def make_addr_lambda(expr: str):
    # Replace register names with direct list access
    for reg, idx in reg_look.items():
        expr = expr.replace(reg, f"cpu.regs[{idx}]")
    code = compile(expr, "<mem>", "eval")
    return lambda: eval(code, {"cpu": cpu})

        
            
comands: list[str] =["mov","add","sub","mul","div","cmp","jmp","jne","jeq","lea","pri"] #pri is definitly asm yeah


lables :dict[str,int]= {}


with open("input.asm","r") as file:
    text: list[str]=file.readlines()

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
            for reg in reg_look:
                texpr = texpr.replace(reg, str(cpu.regs[reg_look[reg]]))

            # Validate: only numbers, + - * allowed now
            if not regex.fullmatch(r"[0-9+\-*()]+", expr):
                raise SyntaxError(f"Invalid memory expression: {expr}")

            # Replace registers with their acces
            for reg in reg_look:
                expr = expr.replace(reg, f"cpu.regs[{reg}]")

            expr_code = compile(expr, "<mem>", "eval")

            nlin.append((2, size, make_addr_lambda(expr)))
            
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
        labels[label] = len(code)-1   # points to *next* instruction index
    else:
        code.append(line)

        


# Pass 2: replace lables by int

for instr in code:
    for j in range(1, len(instr)):   # look at operands
        if isinstance(instr[j], str) and instr[j] in labels:
            instr[j] = (0, labels[instr[j]])

    

        


# Pass 3: execution loop

print(code)

start_time: float = time.perf_counter()


def op_mov (a,b): write_val(a,get_val(b))
def op_inc (a): cpu.alu.inc(a)
def op_neg (a): cpu.alu.neg(a)
def op_shl (a,b): cpu.alu.shl(a,b)
def op_shr (a,b): cpu.alu.shr(a,b)
def op_add (a,b): cpu.alu.add(a,b)
def op_sub (a,b): cpu.alu.sub(a,b)
def op_mul (a,b): cpu.alu.mul(a,b)
def op_div (a,b): cpu.alu.div(a,b)
def op_cmp (a,b): cpu.alu.cmp(a,b)
def op_jmp (a): cpu.alu.branch.jmp(a)
def op_jne (a): cpu.alu.branch.jne(a)
def op_je  (a): cpu.alu.branch.je(a)
def op_jmg (a): cpu.alu.branch.jmp(a)
def op_pri (a): print(get_val(a))



oplist = [
    op_mov,
    op_inc,
    op_neg,
    op_shl,
    op_shr,
    op_add,
    op_sub,
    op_mul,
    op_div,
    op_cmp,
    op_jmp,
    op_jne,
    op_je ,
    op_jmg,
    op_pri
]
    
i=0
# Execution loop
while i < len(code):
    instr = code[i]
    oplist[instr[0]](*instr[1:]) # type: ignore
    i += 1

end_time: float = time.perf_counter()
print(f"Execution time: {end_time - start_time:.6f} seconds")