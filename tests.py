import assembler
import vm

def call_ret_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/callret_test.pvm', 'testing/callret_test.pal')
    test_prog = assembler.read_pvm_file('testing/callret_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 40

def jmp_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/jmp_test.pvm', 'testing/jmp_test.pal')
    test_prog = assembler.read_pvm_file('testing/jmp_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 40

def je_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/je_test.pvm', 'testing/je_test.pal')
    test_prog = assembler.read_pvm_file('testing/je_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 40

def jn_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/jn_test.pvm', 'testing/jn_test.pal')
    test_prog = assembler.read_pvm_file('testing/jn_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 40

def jl_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/jl_test.pvm', 'testing/jl_test.pal')
    test_prog = assembler.read_pvm_file('testing/jl_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 40

def jg_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/jg_test.pvm', 'testing/jg_test.pal')
    test_prog = assembler.read_pvm_file('testing/jg_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 40

def loop_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/loop_test.pvm', 'testing/loop_test.pal')
    test_prog = assembler.read_pvm_file('testing/loop_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 110

def seth_pushfh_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/seth_pushfh_test.pvm', 'testing/seth_pushfh_test.pal')
    test_prog = assembler.read_pvm_file('testing/seth_pushfh_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 50

def popth_pop_pushfh_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/popth_pop_pushfh_test.pvm', 'testing/popth_pop_pushfh_test.pal')
    test_prog = assembler.read_pvm_file('testing/popth_pop_pushfh_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 67

def movth_add_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/movth_add_test.pvm', 'testing/movth_add_test.pal')
    test_prog = assembler.read_pvm_file('testing/movth_add_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 3000

def cpyh_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/cpyh_test.pvm', 'testing/cpyh_test.pal')
    test_prog = assembler.read_pvm_file('testing/cpyh_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 500

def stkth_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/stkth_test.pvm', 'testing/stkth_test.pal')
    test_prog = assembler.read_pvm_file('testing/stkth_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 255

def pshfhh_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/pshfhh_test.pvm', 'testing/pshfhh_test.pal')
    test_prog = assembler.read_pvm_file('testing/pshfhh_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 566

def pshfhs_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/pshfhs_test.pvm', 'testing/pshfhs_test.pal')
    test_prog = assembler.read_pvm_file('testing/pshfhs_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 560

def pop2_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/pop2_test.pvm', 'testing/pop2_test.pal')
    test_prog = assembler.read_pvm_file('testing/pop2_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 2535

def popn_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/popn_test.pvm', 'testing/popn_test.pal')
    test_prog = assembler.read_pvm_file('testing/popn_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 307

def arithmetic_test(use_debug_mode=False):
    assembler.build_pvm_file('testing/arithmetic_test.pvm', 'testing/arithmetic_test.pal')
    test_prog = assembler.read_pvm_file('testing/arithmetic_test.pvm')
    return vm.exec(test_prog, 200, 200, 200, use_debug_mode) == 200


def test_all(use_debug_mode=False):
    all_passed = True
    passed_tests = 0
    test_count = 17

    call_ret_test_result = call_ret_test(False)
    jmp_test_result = jmp_test(False)
    je_test_result = je_test(False)
    jn_test_result = jn_test(False)
    jl_test_result = jl_test(False)
    jg_test_result = jg_test(False)
    loop_test_result = loop_test(False)
    seth_pushfh_test_result = seth_pushfh_test(False)
    popth_pop_pushfh_test_result = popth_pop_pushfh_test(False)
    movth_add_test_result = movth_add_test(False)
    cpyh_test_result = cpyh_test(False)
    stkth_test_result = stkth_test(False)
    pshfhh_test_result = pshfhh_test(False)
    pshfhs_test_result = pshfhs_test(False)
    pop2_test_result = pop2_test(False)
    popn_test_result = popn_test(False)
    arithmetic_test_result = arithmetic_test(False)

    if call_ret_test_result:
        passed_tests += 1
        print('\ncall_ret_test passed')
    else:
        all_passed = False
        print('\ncall_ret_test failed <================================')

    if jmp_test_result:
        passed_tests += 1
        print('jmp_test passed')
    else:
        all_passed = False
        print('jmp_test failed <================================')

    if je_test_result:
        passed_tests += 1
        print('je_test passed')
    else:
        all_passed = False
        print('je_test failed <================================')

    if jn_test_result:
        passed_tests += 1
        print('jn_test passed')
    else:
        all_passed = False
        print('jn_test failed <================================')

    if jl_test_result:
        passed_tests += 1
        print('jl_test passed')
    else:
        all_passed = False
        print('jl_test failed <================================')

    if jg_test_result:
        passed_tests += 1
        print('jg_test passed')
    else:
        all_passed = False
        print('jg_test failed <================================')

    if loop_test_result:
        passed_tests += 1
        print('loop_test passed')
    else:
        all_passed = False
        print('loop_test failed <================================')

    if seth_pushfh_test_result:
        passed_tests += 1
        print('seth_pushfh_test passed')
    else:
        all_passed = False
        print('seth_pushfh_test failed <================================')

    if popth_pop_pushfh_test_result:
        passed_tests += 1
        print('popth_pop_pushfh_test passed')
    else:
        all_passed = False
        print('popth_pop_pushfh_test failed <================================')

    if movth_add_test_result:
        passed_tests += 1
        print('movth_add_test passed')
    else:
        all_passed = False
        print('movth_add_test failed <================================')

    if cpyh_test_result:
        passed_tests += 1
        print('cpyh_test passed')
    else:
        all_passed = False
        print('cpyh_test failed <================================')

    if stkth_test_result:
        passed_tests += 1
        print('stkth_test passed')
    else:
        all_passed = False
        print('stkth_test failed <================================')

    if pshfhh_test_result:
        passed_tests += 1
        print('pshfhh_test passed')
    else:
        all_passed = False
        print('pshfhh_test failed <================================')

    if pshfhs_test_result:
        passed_tests += 1
        print('pshfhs_test passed')
    else:
        all_passed = False
        print('pshfhs_test failed <================================')

    if pop2_test_result:
        passed_tests += 1
        print('pop2_test passed')
    else:
        all_passed = False
        print('pop2_test failed <================================')

    if popn_test_result:
        passed_tests += 1
        print('popn_test passed')
    else:
        all_passed = False
        print('popn_test failed <================================')

    if arithmetic_test_result:
        passed_tests += 1
        print('arithmetic test passed')
    else:
        all_passed = False
        print('arithmetic test failed <================================')

    print('\n%d/%d tests passed.' % (passed_tests, test_count))

    return all_passed

def main():
    test_all(False)


#main()