import re as regex

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

        def add(self, a:str, b:str) -> None:
            write_val(a,get_val(a) + get_val(b))

        def sub(self, a:str, b:str) -> None:
            write_val(a,get_val(a) - get_val(b))

        def mul(self, a:str, b:str) -> None:
            write_val(a,get_val(a) * get_val(b))

        def div(self, a:str, b:str) -> None:
            write_val(a,get_val(a) // get_val(b))

        def cmp(self, a, b) -> None:
            self.flags["zf"] = (a == b)
            self.flags["gf"] = (a > b)
            self.flags["lf"] = (a < b)





cpu=ccpu()

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
        return cpu.mem.read_mem(get_val(exp),sizes[meml[0]])
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
    code.append(parse(line))

print(code)

# Pass 1: collect labels
for idx, line in enumerate(code):
    if line[0].endswith(":"):
        if line[0] in lables:
            raise SyntaxError(f"Duplicate label: {line[0]}")
        lables[line[0]] = idx

# Pass 2: execution loop

i=0
while i < len(code) :
    ccl:str=code[i][0]  #curent code line
    
    match ccl:
        case "mov":
            write_val(code[i][1],get_val(code[i][2]))

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


        case "pri":
            print(get_val(code[i][1]))
    
    if ccl.endswith(":"):
        if ccl in lables.keys():
            raise SyntaxError("cant reasinge a lable: {cll}")
        
        lables[ccl]=i

    i+=1





