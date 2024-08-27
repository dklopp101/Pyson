import assembler

return_codes = {'success' : 0, 'invalidOpcode' : 1, 'zeroDivisionError' : 2}
return_codemap = {value: key for key, value in return_codes.items()}

def exec(prog, heapSize, workStackSize, callStackSize, debug_mode=False):
    # Initialise some control vars used by the vm.
    cycle_count = 0
    buff_1 = 0
    buff_2 = 0
    cmp_flag = 0

    # Initialise the program counter to the starting instruction's address.
    # prog[0] always contains a list containing the starting address and programs list length.
    # so start address is found at prog[0][0] and length found at prog[0][1].
    pc = prog[0][0]
    last_pc = 0

    # Initialise data structures.
    workStack = [0] * workStackSize
    workStackTop = 0

    callStack = [0] * callStackSize
    callStackTop = 0

    loop_counter = 0
    loop_body_addr = 0
    loop_end_addr = 0

    heap = [0] * heapSize

    # main runtime loop.
    # instruction is fetched via prog[pc][0], prog[pc] is the current instruction, prog[pc][0] would be the opcode,
    # prog[pc][1], prog[pc][2] and so on would be its operands.
    while True:
        #if debug_mode: print('entered main loop.')
        cycle_count += 1
        last_pc = pc

        # DIE INSTRUCTION.
        if prog[pc][0] == 0:
            if debug_mode:
                print('DIE BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            return 0

        # NOP INSTRUCTION.
        elif prog[pc][0] == 1:
            if debug_mode:
                print('NOP BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            pc += 1

        # CALL INSTRUCTION.
        elif prog[pc][0] == 2:
            if debug_mode:
                print('CALL BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            callStackTop += 1
            callStack[callStackTop] = pc + 1 # push return address(next instruction after this CALL instruction) onto call stack.
            pc = prog[pc][1] # set pc to call address.

        # RET INSTRUCTION.
        elif prog[pc][0] == 3:
            if debug_mode:
                print('RET BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            pc = callStack[callStackTop] # set pc to return addr
            callStackTop -= 1 # pop ret addr off callstack

        # JMP INSTRUCTION.
        elif prog[pc][0] == 4:
            if debug_mode:
                print('JMP BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            pc = prog[pc][1] # set pc to jmp addr which is operand 1 of this JMP instruction.

        # JEQ INSTRUCTION.
        elif prog[pc][0] == 5:
            if debug_mode:
                print('JEQ BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            if cmp_flag == 0: # check if top 2 values on stack are equal.
                pc = prog[pc][1] # set pc to jmp addr
            else:
                pc += 1

        #JNEQ INSTRUCTION.
        elif prog[pc][0] == 6:
            if debug_mode:
                print('JNEQ BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            if cmp_flag: # check if top 2 values on stack are equal.
                pc = prog[pc][1] # set pc to jmp addr
            else:
                pc += 1

        #JLT INSTRUCTION.
        elif prog[pc][0] == 7:
            if debug_mode:
                print('JL BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            if cmp_flag == 1: # check if top 2 values on stack are equal.
                pc = prog[pc][1] # set pc to jmp addr
            else:
                pc += 1

        #JGT INSTRUCTION.
        elif prog[pc][0] == 8:
            if debug_mode:
                print('JGT BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            if cmp_flag == 2: # check if top 2 values on stack are equal.
                pc = prog[pc][1] # set pc to jmp addr
            else:
                pc += 1

        # LOOP INSTRUCTION
        elif prog[pc][0] == 9:
            if debug_mode:
                print('LOOP BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            loop_end_addr = prog[pc][1] # push loop end onto loop stack.
            loop_body_addr = prog[pc][2] # push loop body onto loop stack.
            loop_counter = workStack[workStackTop] # push iter count from top of work stack onto loop stack.

            pc = loop_body_addr # set pc to loop body addr.

        # LCONT INSTRUCTION
        elif prog[pc][0] == 10:
            if debug_mode:
                print('LCONT BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            if loop_counter != 1: # check if loop count has been reached.
                loop_counter -= 1 # decrement iteration counter.
                pc = loop_body_addr # set pc to loop body addr.

            else: # iteration count was zero so loop has ended.
                pc = loop_end_addr # set pc to loop end addr.

        # LBRK INSTRUCTION
        elif prog[pc][0] == 11:
            if debug_mode:
                print('LBRK BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            pc = loop_end_addr

        # PUSH INSTRUCTION
        elif prog[pc][0] == 12:
            if debug_mode:
                print('PUSH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStackTop += 1
            workStack[workStackTop] = prog[pc][1] # push value onto work stack.
            pc += 1

        # POP INSTRUCTION
        elif prog[pc][0] == 13:
            if debug_mode:
                print('POP BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStackTop -= 1 # "pop" value off the stack.
            pc += 1

        # POP2 INSTRUCTION
        elif prog[pc][0] == 14:
            if debug_mode:
                print('POP2 BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStackTop -= 2 # "pop" two values off the stack.
            pc += 1

        # POPN INSTRUCTION
        elif prog[pc][0] == 15:
            if debug_mode:
                print('POPN BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStackTop -= prog[pc][1] # "pop" n values off the stack.
            pc += 1

        # PUSHFH INSTRUCTION
        elif prog[pc][0] == 16:
            if debug_mode:
                print('PUSHFH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStackTop += 1
            workStack[workStackTop] = heap[prog[pc][1]]
            pc += 1

        # POPTH INSTRUCTION
        elif prog[pc][0] == 17:
            if debug_mode:
                print('POPTH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            heap[prog[pc][1]] = workStack[workStackTop] # set specified heap addr to top of stack
            workStackTop -= 1 # pop value off the stack.
            pc += 1

        # MOVTH INSTRUCTION
        elif prog[pc][0] == 18:
            if debug_mode:
                print('MOVTH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            heap[prog[pc][1]] = workStack[workStackTop] # set specified heap address to be value at top of stack.
            pc += 1

        # STKTH INSTRUCTION
        elif prog[pc][0] == 19:
            if debug_mode:
                print('STKTH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            heap[prog[pc][1]] = workStack[prog[pc][2]] # set specified heap address to be value at specified stack address.
            pc += 1

        # COPYH INSTRUCTION
        elif prog[pc][0] == 20:
            if debug_mode:
                print('COPYH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            heap[prog[pc][1]] = heap[prog[pc][2]] # set specified heap address to value at other specified heap address.
            pc += 1

        # SETH INSTRUCTION
        elif prog[pc][0] == 21:
            if debug_mode:
                print('SETH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            heap[prog[pc][1]] = prog[pc][2] # set specified heap address to value in operand 2 of SETH instruction.
            pc += 1

        # PSHFHH INSTRUCTION
        elif prog[pc][0] == 22:
            if debug_mode:
                print('PSHFHH BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            # use operand as address of heap slot who's value we use as address to
            # another heap slot who's value we push onto the stack.
            workStackTop += 1
            workStack[workStackTop] = heap[heap[prog[pc][1]]]
            pc += 1

        # PSHFHS INSTRUCTION
        elif prog[pc][0] == 23:
            if debug_mode:
                print('PSHFHS BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            # use value at stack top as address for heap slot who's value we use
            # as address for another heap slot who's value we push onto stack.
            workStack[workStackTop+1] = heap[heap[workStack[workStackTop]]]
            workStackTop += 1
            pc += 1

        # CMP INSTRUCTION
        elif prog[pc][0] == 24:
            if debug_mode:
                print('CMP BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            if workStack[workStackTop] == workStack[workStackTop-1]:
                cmp_flag = 0 # values are equal.
            elif workStack[workStackTop] < workStack[workStackTop-1]:
                cmp_flag = 1 # value1(top) is less than value2(top-1)
            else:
                cmp_flag = 2 # value1(top) is greater than value2(top-1)
            pc += 1

        # INC INSTRUCTION
        elif prog[pc][0] == 25:
            if debug_mode:
                print('INC BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStack[workStackTop] += 1
            pc += 1

        # DEC INSTRUCTION
        elif prog[pc][0] == 26:
            if debug_mode:
                print('INC BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStack[workStackTop] -= 1
            pc += 1

        # ADD INSTRUCTION
        elif prog[pc][0] == 27:
            if debug_mode:
                print('ADD BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStack[workStackTop+1] = workStack[workStackTop] + workStack[workStackTop-1]
            workStackTop += 1
            pc += 1

        # SUB INSTRUCTION
        elif prog[pc][0] == 28:
            if debug_mode:
                print('SUB BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStack[workStackTop+1] = workStack[workStackTop] - workStack[workStackTop-1]
            workStackTop += 1
            pc += 1

        # MUL INSTRUCTION
        elif prog[pc][0] == 29:
            if debug_mode:
                print('MUL BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            workStack[workStackTop+1] = workStack[workStackTop] * workStack[workStackTop-1]
            workStackTop += 1
            pc += 1

        # DIV INSTRUCTION
        elif prog[pc][0] == 30:
            if debug_mode:
                print('DIV BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            try:
                workStack[workStackTop + 1] = int(workStack[workStackTop] / workStack[workStackTop - 1])
            except ZeroDivisionError:
                return 2
            workStackTop += 1
            pc += 1

        # MOD INSTRUCTION
        elif prog[pc][0] == 31:
            if debug_mode:
                print('MOD BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            try:
                workStack[workStackTop + 1] = workStack[workStackTop] % workStack[workStackTop - 1]
            except ZeroDivisionError:
                return 2
            workStackTop += 1
            pc += 1

        # NSPCT INSTRUCTION
        # container codes: 1 workstack, 2 heap, 3 cstack, 4 lstack, 5 prog
        # print codes: -2 print all, -1 print stacktop, n print container[n]
        elif prog[pc][0] == 32:
            if debug_mode:
                print('NSPCT BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            # determine what we are inspecting
            if prog[pc][1] == 1: # workStack
                if prog[pc][2] == -2: # are we printing entire thing
                    for addr, value in enumerate(workStack):
                        print("\nstack[%d] = %d" % (addr, value))
                elif prog[pc][2] == -1: # printing stack top.
                    print("stack top: %d" % workStack[workStackTop])
                else:
                    print("\nstack[%d] = %d" % (prog[pc][2], workStack[prog[pc][2]]))

            elif prog[pc][1] == 2: # heap
                if prog[pc][2] == -2: # are we printing entire thing
                    for addr, value in enumerate(heap):
                        print("\nheap[%d] = %d" % (addr, value))
                elif prog[pc][2] == -1: # printing loop stack top.
                    print("tried to print heap top error")
                else:
                    print("\nheap[%d] = %d" % (prog[pc][2], heap[prog[pc][2]]))

            elif prog[pc][1] == 3: # call stack.
                if prog[pc][2] == -2: # are we printing entire thing
                    for addr, value in enumerate(callStack):
                        print("\ncall stack[%d] = %d" % (addr, value))
                elif prog[pc][2] == -1: # printing loop stack top.
                    print("call stack top: %d" % callStack[callStackTop])
                else:
                    print("\ncall stack[%d] = %d" % (prog[pc][2], callStack[prog[pc][2]]))

            elif prog[pc][1] == 4: # program
                if prog[pc][2] == -2: # are we printing entire thing
                    for addr, value in enumerate(prog):
                        print("\nprog[%d] = %d" % (addr, value))
                elif prog[pc][2] == -1: # printing loop stack top.
                    print("tried to print prog top error")
                else:
                    print("\nprog[%d] = %d" % (prog[pc][2], prog[prog[pc][2]]))

            else:
                print("NSPCT INSTRUCTION OPERAND INVALID!")

            pc += 1

        #NSPCTST INSTRUCTION.
        elif prog[pc][0] == 33:
            if debug_mode:
                print('NSPCTST BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            print('stack-top = %d' % workStack[workStackTop])
            pc += 1

        #TEST_DIE
        elif prog[pc][0] == 34:
            if debug_mode:
                print('TEST_DIE BLOCK.')
                debug_print(cycle_count, last_pc, prog[pc], prog[pc][0])

            return workStack[workStackTop]

        # Opcode doesn't match any instruction.
        else:
            if debug_mode:
                print("Invalid operation code, %d, on cycle %d" % (prog[pc][0], cycle_count))
            return 1

def debug_print(cycle_count, last_pc, instr, opcode):
    debug_str = 'cycle: %d executed addr[%d] op: %s(opcode: %d) operands: (' % (cycle_count, last_pc, assembler.reversed_opmap[opcode], opcode)

    if len(instr) > 1:
        for i in instr[1:]:
            debug_str += ' %d' % i

    print('%s )' % debug_str)

def main():
    prog = assembler.read_pvm_file('call_test.pvm')
    x = exec(prog, 20, 20, 20, 20, True)
    print('pvm return state: %s' % return_codemap[x])

#main()