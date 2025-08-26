; Benchmark program
start:
    mov rax, 0
    mov rbx, 1
    mov rcx, 1000000     ; loop counter

loop:
    add rax, rbx         ; rax = rax + rbx
    sub rcx, 1           ; rcx -= 1
    jne loop:            ; if rcx != 0, repeat

end:
    pri rax              ; print final result
