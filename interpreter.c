#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include "mem.h"



enum { IMM=0, REG=1, MEM=2 };

int64_t regs[]={0,0,0,0,0,0,0,0,0,0,0,0};

uint8_t mem[1000010];

bool zf= false;
bool sf= false;


/*
"zf": False,  # zero flag
"gf": False,  # greater flag
"lf": False,  # less flag
*/

int64_t read_mem(size_t adr, uint8_t size) {
    //printf("read: addr: %zu size:%u",adr,size);
    switch (size) {
        case 0: return *(int8_t*)(mem + adr);
        case 1: return *(int16_t*)(mem + adr);
        case 2: return *(int32_t*)(mem + adr);
        case 3: return *(int64_t*)(mem + adr);
        default: return 0; // error
    }
}

void write_mem(size_t adr, uint8_t size, int64_t val) {
    //printf("write: addr: %zu size:%u val: %lld\n",adr,size,val);
    switch (size) {
        case 0: *(int8_t*)(mem + adr) = (int8_t)val; break;
        case 1: *(int16_t*)(mem + adr) = (int16_t)val; break;
        case 2: *(int32_t*)(mem + adr) = (int32_t)val; break;
        case 3: *(int64_t*)(mem + adr) = (int64_t)val; break;
    }
}

static inline void set_flags(int result){
    zf= !result;
    sf= (result<0);
}


static inline int64_t get_val(uint8_t mode, int val) {
    if (mode == IMM) return val;
    if (mode == REG) return regs[val];
    if (mode == MEM){
        uint32_t u = (uint32_t)val;
        uint8_t size = (uint8_t)(u >> 30);
        uint32_t num = u & ((1u << 30) - 1);

        return read_mem(mem_table[num](),size);
    }
    return 1;
}
static inline void write_val(uint8_t mode, int val, int64_t wval) {
    if (mode == REG) regs[val] = wval;
    if (mode == MEM){
        uint32_t u = (uint32_t)val;
        uint8_t size = (uint8_t)(u >> 30);
        uint32_t num = u & ((1u << 30) - 1);

        write_mem(mem_table[num](),size,wval);
    }
}

typedef struct {
    uint8_t op;   // opcode
    uint8_t m1;   // operand 1 mode
    uint8_t m2;   // operand 2 mode
    int32_t v1;   // operand 1 value
    int32_t v2;   // operand 2 value
} Instr;


Instr *decode(uint8_t *code, size_t size, size_t *out_count) {
    size_t n = size / 11; // since each instr = 1 + (1+4)*2 = 11 bytes
    Instr *prog = malloc(n * sizeof(Instr));
    size_t ip = 0;
    for (size_t i = 0; i < n; i++) {
        prog[i].op = code[ip++];
        prog[i].m1 = code[ip++];
        prog[i].v1 = *(int32_t*)(code + ip); ip += 4;
        prog[i].m2 = code[ip++];
        prog[i].v2 = *(int32_t*)(code + ip); ip += 4;
    }
    *out_count = n;
    return prog;
}




int main(){
  
    
    FILE *f = fopen("C:/Users/Levi/Documents/GitHub/asm_interpreter/program.bin", "rb");
    if (!f) return -1;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    rewind(f);


    uint8_t *code = malloc(size);
    fread(code, 1, size, f);
    fclose(f);

    // now `code` holds the whole bytecode stream

    

    int result = 0;

    

    /*
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
    */

    size_t n_instrs;
    Instr *prog = decode(code, size, &n_instrs);

    clock_t start = clock();
    size_t ip = 0;
    while (ip < n_instrs ){

        Instr in = prog[ip];

        //printf("op: %d, ip:%d \n",in.op,ip);

        

        switch (in.op){
            case 0:
                //mov
                

                write_val(in.m1,in.v1,get_val(in.m2,in.v2));

                break;
            case 1:
                //inc


                write_val(in.m1,in.v1,get_val(in.m1,in.v1)+1);
                
                break;
            
            case 2:
                //dec

                write_val(in.m1,in.v1,get_val(in.m1,in.v1)-1);
                
                break;

            case 3:
                //neg
                

                write_val(in.m1,in.v1,get_val(in.m1,in.v1)*-1);
                
                break;
            case 4:
                //shl
                

                result = get_val(in.m1,in.v1) << get_val(in.m2,in.v2);
                set_flags(result);

               
                write_val(in.m1,in.v1,result);
                
                break;
            case 5:
                //shr
                

                result = get_val(in.m1,in.v1) >> get_val(in.m2,in.v2);
                set_flags(result);

               
                write_val(in.m1,in.v1,result);

                
                break;
            case 6:
                //add
                

                result = get_val(in.m1,in.v1)+get_val(in.m2,in.v2);
                set_flags(result);

               
                write_val(in.m1,in.v1,result);

                
                break;
            case 7:
                //sub
                

                result = get_val(in.m1,in.v1)-get_val(in.m2,in.v2);
                set_flags(result);

               
                write_val(in.m1,in.v1,result);

                
                break;
            case 8:
                //mul
                

                result = get_val(in.m1,in.v1)*get_val(in.m2,in.v2);
                set_flags(result);

               
                write_val(in.m1,in.v1,result);

                
                break;
            case 9:
                //div
                

                result = get_val(in.m1,in.v1)/get_val(in.m2,in.v2);
                set_flags(result);

               
                write_val(in.m1,in.v1,result);

                
                break;

            case 10:
                //cmp


                set_flags(get_val(in.m1,in.v1)-get_val(in.m2,in.v2));
                
                break;

            case 11:
                //jmp

                ip = (size_t)get_val(in.m1,in.v1);
                continue;
                
                
                break;
            case 12:
                //jne
                if (!zf){
                    ip = (size_t)get_val(in.m1,in.v1);
                    continue;
                }
                
                
                break;
            
            case 13:
                //je
                if (zf){
                    ip = (size_t)get_val(in.m1,in.v1);
                    continue;
                }
                
                
                
                break;

            case 14:
                //jg
                if (!zf){
                    ip = (size_t)get_val(in.m1,in.v1);
                    continue;
                }
                
                
                break;

            case 15:
                //jl
                if (zf){
                    ip = (size_t)get_val(in.m1,in.v1);
                    continue;
                }
                
                
                break;
            
            case 16:
                //pri
                printf("%lld " , (int64_t)get_val(in.m1, in.v1));
                break;
            default:
                return -1;
                break;
        }

        ip++;

        /*
    "mov": 0,
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
    "pri": 16,
    */
        





    }
    clock_t stop = clock();
    double elapsed = (double)(stop - start) * 1000.0 / CLOCKS_PER_SEC;
    printf("\nTime elapsed in ms: %f", elapsed);
    
}