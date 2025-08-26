import re as regex
import time

i=0

class ccpu:
    def __init__(self) -> None:
        self.regs: dict[str, int] = {
            "rax": 0,
            "rbx": 0,
            "rcx": 0,
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
    

    # Safe eval
    return eval(expr)

sizes: dict[str, int] = {"byte":1,"word":2,"dword":4,"qword":8}

def get_val(tex:str) -> int:
    if tex.isnumeric():
        return int(tex)

    elif tex in cpu.regs:
        return cpu.regs[tex]
        
    elif tex.split(" ",2)[1] == "ptr":
        meml: list[str] = tex.split(" ")
        addr = eval_address(meml[2] )

        return cpu.mem.read_mem(addr, sizes[meml[0]])
    
    else:
        raise SyntaxError("balls")

    

def write_val(were:str,val:int) -> None:
    if were in cpu.regs:
        cpu.regs[were] = val

    elif were.split(" ",2)[1] == "ptr":
        meml: list[str] = were.split(" ",2)
        exp: str=meml[2]
        cpu.mem.write_mem(val,get_val(exp),sizes[meml[0]])

    else:
        raise SyntaxError("ligma")




        
            
comands: list[str] =["mov","add","sub","mul","div","cmp","jmp","jne","jeq","lea","pri"] #pri is definitly asm yeah


lables :dict[str,int]= {}


with open("input.asm","r") as file:
    text: list[str]=file.readlines()

def parse(line:str )->list[str]:
    lin: list[str] = line.replace(",", " ").split()
    nlin: list[str] = []
    i=0
    while i  < len(lin):
        if lin[i] in sizes.keys() and i < (len(lin)-2):
            sumline: str = lin[i]+" "
            sumline+=lin[i+1]+" "
            expr: str = lin[i+2][1:-1]

            expr = expr.replace(" ", "")
            texpr = str(expr)

            # Replace registers with their numeric values
            for reg in cpu.regs:
                texpr = texpr.replace(reg, str(cpu.regs[reg]))

            # Validate: only numbers, + - * allowed now
            if not regex.fullmatch(r"[0-9+\-*()]+", expr):
                raise SyntaxError(f"Invalid memory expression: {expr}")

            # Replace registers with their acces
            for reg in cpu.regs:
                expr = expr.replace(reg, f"cpu.regs[{reg}]")

            

            sumline+=expr
            nlin.append(sumline)
            i+=3
        elif lin[i].startswith(";"):
            return nlin

        elif lin[i]:
            
            nlin.append(lin[i])
            i+=1

        else:
            i+=1

    return nlin

code:list[str] = []

for line in text:
    laa: list[str]=parse(line)
    if laa:
        code.append(laa)  # type: ignore



# Pass 1: collect labels
for idx, line in enumerate(code):
    if line[0].endswith(":"):
        if line[0] in lables:
            raise SyntaxError(f"Duplicate label: {line[0]}")
        lables[line[0]] = idx

# Pass 3: replace lables by int

for i in range(len(code)):
    if len(code[i]) > 1:
        
        if code[i][1] in lables:
            print("sigma")
            code[i][1] = str(lables[code[i][1]]) # type: ignore

        if len(code[i]) > 2:
            if code[i][2] in lables:
                code[i][2] = str(lables[code[i][2]]) # type: ignore
    

        


# Pass 3: execution loop

print(code)

start_time: float = time.perf_counter()

i:int=0
while i < len(code) :
    
    instr = code[i]
    op: str = instr[0]

    #print(f"isp: {i}")

    
    match op:
        case "mov":
            write_val(code[i][1],get_val(code[i][2]))

        case "lea":
            write_val(code[i][1],eval_address(code[i][2][1:-1]))


        case "inc":
            cpu.alu.inc(code[i][1])

        case "neg":
            cpu.alu.neg(code[i][1])

        case "shl":
            cpu.alu.shl(code[i][1],code[i][2])

        case "shr":
            cpu.alu.shr(code[i][1],code[i][2])

        case "add":
            cpu.alu.add(code[i][1],code[i][2])

        case "sub":
            cpu.alu.sub(code[i][1],code[i][2])

        case "mul":
            cpu.alu.mul(code[i][1],code[i][2])

        case "div":
            cpu.alu.div(code[i][1],code[i][2])


        case "cmp":
            cpu.alu.cmp(get_val(code[i][1]),get_val(code[i][2]))

        case "jmp":
            cpu.alu.branch.jmp(code[i][1])

        case "jne":
            cpu.alu.branch.jne(code[i][1])

        case "je":
            cpu.alu.branch.je(code[i][1])

        case "jmp":
            cpu.alu.branch.jmp(code[i][1])


        case "pri":
            print(get_val(code[i][1]))
    

    i+=1

end_time: float = time.perf_counter()
print(f"Execution time: {end_time - start_time:.6f} seconds")