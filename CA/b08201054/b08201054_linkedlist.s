.globl __start
.rodata
    zero_element: .string "Empty!"

# slt x11, zero, s0
.text
__start:
    # Read first operand
    li a0, 5
    ecall
    mv x11, a0
    beq x11, zero, zero_element_exp 
    # x11 is number of nodes
    # x12 : loop index 
    add x12, zero, zero
    # x13 for base register of linled list
    add x13, sp, zero
    # addi sp, sp, 80000

Loop: 
  # x11==n >= 12 -> do x11 times
  bge x12, x11, foo  
  
  li a0, 5
  ecall
  # x14 for template registet
  mv x14, a0
  sw x14, 0(sp)
  
  addi x12, x12, 1
  addi sp, sp, -8
  j Loop

# addi x13, x13, 8
# addi x12, x12, 1

foo:
  addi x13, x13, 8
  addi x12, x12, 1
Print_list:  
  # beq x12, zero, exit
  addi x13, x13, -8
  addi x12, x12, -1
  beq x12, zero, exit
  li a0, 1
  lw x11, 0(x13)
  mv a1, x11
  ecall
  
  li a0, 11
  li a1, ' '
  ecall 

  j Print_list

zero_element_exp:
    li a0, 4
    la a1, zero_element 
    ecall 
    jal zero, exit
exit:
    # Exit program(necessary)
    li a0, 10
    ecall
