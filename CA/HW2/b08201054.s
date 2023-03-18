.globl __start

.rodata
    division_by_zero: .string "division by zero"

.text
__start:
    # Read first operand
    li a0, 5
    ecall
    mv s0, a0
    # Read operation
    li a0, 5
    ecall
    mv s1, a0
    # Read second operand
    li a0, 5
    ecall
    mv s2, a0
    
    # first (operand, operation, operand) stored as (s0, s1, s2)

###################################
#  TODO: Develop your calculator  #
#                                 #
###################################

# operation : stores at s1

# check s1 >= 0 and s1 < 7
slt t1, s1, zero
bne t1, zero, exit

slti t1, s1, 7
beq t1, zero, exit

# if s1 == 0 : goto add
add t2, zero, zero
sub t1, s1, t2
beq t1, zero, op_0

# else if s1 == 1 : goto sub
addi t2, zero, 1
sub t1, s1, t2
beq t1, zero, op_1

# else if s1 == 2 : goto mul
addi t2, zero, 2
sub t1, s1, t2
beq t1, zero, op_2

# else if s1 == 3 : goto div
addi t2, zero, 3
sub t1, s1, t2
beq t1, zero, op_3

# else if s1 == 4 : min(s0, s3)
addi t2, zero, 4
sub t1, s1, t2
beq t1, zero, op_4

# else if s1 == A^B
addi t2, zero, 5
addi s3, zero, 1
beq t2, s1, op_5

# else if s1 == A!
addi t2, zero, 6
addi s3, zero, 1
beq t2, s1, op_6


op_0: # add
  add s3, s2, s0
  beq zero, zero, output
  
op_1: # sub
  sub s3, s0, s2
  beq zero, zero, output

op_2:
  mul s3, s0, s2
  beq zero, zero, output

op_3:
  # check divide error
  beq s2, zero, division_by_zero_except
  div s3, s0, s2
  j output

op_4: # min(s0, s2)
  slt t2, s0, s2 # s0 < s2 ? 
  bne t2, zero, set_1 # if t2 != 0, i.e. s0 >= s2 
  beq t2, zero, set_2

op_5:
  beq s2, zero, output
  mul s3, s3, s0
  addi s2, s2, -1
  j op_5

op_6:
  beq s0, zero, output
  mul s3, s3, s0
  addi s0, s0, -1
  j op_6
  
set_1:
  add s3, zero, s0
  beq zero, zero, output
set_2:
  add s3, zero, s2
  beq zero, zero, output
  
output:
    # Output the result
    li a0, 1
    mv a1, s3
    ecall

exit:
    # Exit program(necessary)
    li a0, 10
    ecall

division_by_zero_except:
    li a0, 4
    la a1, division_by_zero
    ecall
    jal zero, exit
    
