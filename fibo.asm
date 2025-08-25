mov r1,0
mov r2,1

mov rax, 10  ;set up counter

start:
mov r3, r2
add r2, r1
mov r1, r3

pri r2  ;print

sub rax, 1
cmp rax, 0
jne start:

