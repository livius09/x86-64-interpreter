extern int64_t regs[];
typedef size_t (*mem_func_t)();

static inline size_t mem_0() { return regs[0]; }

static mem_func_t mem_table[] = {mem_0,};