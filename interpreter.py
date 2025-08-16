import re

class ccpu:
    def __init__(self) -> None:
        self.regs: dict[str, int] = {
            "rax": 0,
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


MEMORY_SIZE = 16 * 1024  # 64 KB
memory = bytearray(MEMORY_SIZE)


cpu=ccpu()

sizes = {"byte":1,"word":2,"dword":4,"qword":8}

def get_val(tex:str) -> int:
    if tex.isnumeric():
        return int(tex)

    elif tex in cpu.regs.keys():
        return cpu.regs[tex]
    
    elif tex.startswith("["):
        return 1
    return int()

def write_val(were:str,val:int) -> None:
    if were in cpu.regs.keys():
        cpu.regs[were] = val



        
            
comands =["mov","add","sub","mul","div","cmp","jmp","jne","jeq","lea","pri"] #pri is definitly asm yeah


with open("input.asm","r") as file:
    text=file.readlines()

code=[]
for line in text:
    code.append(re.split(r'[ ,\s]+',line))
    
print(code)

i=0
while i < len(code) :
    match code[i][0]:
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

    i+=1





