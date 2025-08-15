import re

class cpu():
    def __init__(self) -> None:
        self.regs:dict[str,int]={"rax":0,
                                 "r0":0,
                                 "r1":0,
                                 "r2":0,
                                 "r3":0,
                                 "r4":0,
                                 "r5":0,
                                 "r6":0,
                                 "r7":0,}


        
    
    class alu():
        def __init__(self) -> None:
            self.flags:dict[str,bool]={"zf":False,  #zero flag the only one i will need |:
                                       "cf":False}
            
        def add(self,a,b):
            pass

        def sub(self,a,b):
            pass

        def mul(self,a,b):
            pass

        def div(self,a,b):
            pass

        
            
comands =["mov","add","sub","mul","div","cmp","jmp","jne","jeq", "pri"] #pri is definitly asm yeah


with open("input.asm","r") as file:
    text=file.readlines()

code=[]
for line in text:
    code.append(re.split(r'[ ,\s]+',line))
    
print(code)

i=0
while True:
    match code[i][0]:
        case "mov":
            pass

        case "add":
            pass

        case "sub":
            pass

        case "mul":
            pass





