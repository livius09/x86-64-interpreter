import re as regex
import time

class ccpu:
    def __init__(self) -> None:
        self.regs: dict[str, int] = {
            "rax": 0,
            "rbx":0,
            "rsp": 0,
            "rbp": 0,
            "r0": 0,
            "r1": 0,
            "r2": 0,
            "r3": 0,
            "r4": 0,
            "r5": 0,
            "r6": 0,
            "r7": 0,
            
        }
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
            self.set_flags(a-b)

        class cbranch:
            def __init__(self, alu) -> None:
                self.alu = alu   # keep reference to ALU

            def jmp(self, a) -> None:
                global i
                i = get_val(a)

            def jne(self, a) -> None:
                if not self.alu.flags["zf"]:   
                    global i
                    i = get_val(a)

            def je(self, a) -> None:
                if self.alu.flags["zf"]:   
                    global i
                    i = get_val(a)

            def jge(self, a) -> None:
                if not self.alu.flags["gf"]:   
                    global i
                    i = get_val(a)
                    





cpu=ccpu()


def eval_address(expr: str) -> int:
    """
    Evaluate x86-style address expressions:
    - [rax]
    - [rbp-8]
    - [rax+rbx*2+16]
    - [rbx*4+32]
    """
    expr = expr.replace(" ", "")

    # Replace registers with their numeric values
    for reg in cpu.regs:
        expr = regex.sub(rf"\b{reg}\b", str(cpu.regs[reg]), expr)

    # Validate: only numbers, + - * allowed now
    if not regex.fullmatch(r"[0-9+\-*()]+", expr):
        raise SyntaxError(f"Invalid memory expression: {expr}")

    # Safe eval
    return eval(expr)

sizes: dict[str, int] = {"byte":1,"word":2,"dword":4,"qword":8}

def get_val(tex:str) -> int:
    if tex.isnumeric():
        return int(tex)

    elif tex in cpu.regs.keys():
        return cpu.regs[tex]
    
    elif tex.endswith(":"):
        if tex in lables.keys():
            return lables[tex]
        else:
            raise SyntaxError(f"lable not defined: {tex}")
        
    elif tex.split(" ",2)[0] in sizes.keys():
        meml: list[str] = tex.split(" ")
        exp: str=meml[2][1:-1]
        size = sizes[meml[0]]
        expr = meml[2][1:-1]      # strip [ ]
        addr = eval_address(expr)
        return cpu.mem.read_mem(addr, size)
    else:
        raise SyntaxError("balls")

    

def write_val(were:str,val:int) -> None:
    if were in cpu.regs.keys():
        cpu.regs[were] = val
    elif were.split(" ",2)[0] in sizes.keys():
        meml: list[str] = were.split(" ",2)
        exp: str=meml[2][1:-1]
        cpu.mem.write_mem(val,get_val(exp),sizes[meml[0]])

    else:
        raise SyntaxError("ligma")



comands: list[str] =["mov","add","sub","mul","div","cmp","jmp","jne","jeq","lea","pri"] #pri is definitly asm yeah


lables :dict[str,int]= {}


with open("input.asm","r") as file:
    text: list[str]=file.readlines()

def parse(liner:str )->list[str]:
    lin: list[str] = regex.split(r'[ ,\s]+',line)
    nlin: list[str] = []
    i=0
    while i  < len(lin):
        if lin[i] in sizes.keys() and i < (len(lin)-2):
            sumline: str = lin[i]+" "
            sumline+=lin[i+1]+" "
            sumline+=lin[i+2]
            nlin.append(sumline)
            i+=3
   
        elif lin[i]:
            
            nlin.append(lin[i])
            i+=1

        else:
            i+=1


    return nlin

code=[]

for line in text:
    laa=parse(line)
    if laa:
        code.append(laa)

print(code)

# Pass 1: collect labels
for idx, line in enumerate(code):
    if line[0].endswith(":"):
        if line[0] in lables:
            raise SyntaxError(f"Duplicate label: {line[0]}")
        lables[line[0]] = idx

# Pass 2: execution loop





# === Instruction implementations ===

def instr_mov(args) -> None:
    write_val(args[0], get_val(args[1]))

def instr_lea(args) -> None:
    write_val(args[0], eval_address(args[1][1:-1]))

def instr_inc(args) -> None:
    cpu.alu.inc(args[0])

def instr_neg(args) -> None:
    cpu.alu.neg(args[0])

def instr_shl(args) -> None:
    cpu.alu.shl(args[0], args[1])

def instr_shr(args) -> None:
    cpu.alu.shr(args[0], args[1])

def instr_add(args) -> None:
    cpu.alu.add(args[0], args[1])

def instr_sub(args) -> None:
    cpu.alu.sub(args[0], args[1])

def instr_mul(args) -> None:
    cpu.alu.mul(args[0], args[1])

def instr_div(args) -> None:
    cpu.alu.div(args[0], args[1])

def instr_cmp(args) -> None:
    cpu.alu.cmp(get_val(args[0]), get_val(args[1]))

def instr_jmp(args) -> None:
    cpu.alu.branch.jmp(args[0])

def instr_jne(args) -> None:
    cpu.alu.branch.jne(args[0])

def instr_je(args) -> None:
    cpu.alu.branch.je(args[0])

def instr_pri(args) -> None:
    print(get_val(args[0]))


# === Dispatcher Table (Strategy Pattern) ===
dispatch_table = {
    "mov": instr_mov,
    "lea": instr_lea,
    "inc": instr_inc,
    "neg": instr_neg,
    "shl": instr_shl,
    "shr": instr_shr,
    "add": instr_add,
    "sub": instr_sub,
    "mul": instr_mul,
    "div": instr_div,
    "cmp": instr_cmp,
    "jmp": instr_jmp,
    "jne": instr_jne,
    "je": instr_je,
    "pri": instr_pri,
}

start_time = time.perf_counter()

i = 0
while i < len(code):
    instr :str = code[i][0]   # opcode
    args :list[str] = code[i][1:]   # operands

    #print(f"isp: {i}, instr={instr}, args={args}")

    if instr in dispatch_table:
        dispatch_table[instr](args)
    elif instr.endswith(":"):
        pass
    else:
        raise SyntaxError(f"Unknown instruction: {instr}")

    i += 1

end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time:.4f} seconds")
