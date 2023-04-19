.globl __start
# slt x11, zero, s0
.text
__start:
    # Read first operand
    li a0, 5
    ecall
    mv s0, a0
    # s0 == N

# main function
main:
  addi x13, zero, 1
  addi x14, zero, 2
  jal x1, T
  
  j output

# T
T: 
# store at stack
  addi sp, sp, -32
  sw s0, 24(sp)
  sw x11, 16(sp)
  sw x1, 8(sp)        
    
  bge s0, x14, L1

  # handle base case 
  slt x11, zero, s0
  addi sp, sp, 32
  jalr x0, 0(x1)

L1: 
  addi s0, s0, -1
  jal x1, T

  add x12, zero, x11
  mul x12, x12, x14

  sw x12, 0(sp)
  lw s0, 24(sp)

  addi s0, s0, -2
  jal x1, T

  lw x12, 0(sp)
  add x11, x12, x11

  lw x1, 8(sp)

  addi sp, sp, 32
  jalr x0, 0(x1)


ret_:
  slt x11, zero, s0
  jalr x0, 0(x1)

output:
    # Output the result
    li a0, 1
    mv a1, x11
    ecall

exit:
    # Exit program(necessary)
    li a0, 10
    ecall
