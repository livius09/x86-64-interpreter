; Memory benchmark: fill + sum
start:
    mov rax, 0          ; address pointer
    mov rcx, 1000000    ; loop counter (1M bytes)

fill_loop:
    mov byte ptr [rax], 1
    add rax, 1
    sub rcx, 1
    jne fill_loop:

    ; now sum them back
    mov rax, 0
    mov rcx, 1000000
    mov rbx, 0          ; accumulator

sum_loop:
    add rbx, byte ptr [rax]
    add rax, 1
    sub rcx, 1
    jne sum_loop:

end:
    pri rbx             ; should print 1000000
