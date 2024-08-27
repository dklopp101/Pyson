import pickle

opmap = {'die'     :  0,
         'nop'     :  1,
         'call'    :  2,
         'ret'     :  3,
         'jmp'     :  4,
         'je'      :  5,
         'jn'      :  6,
         'jl'      :  7,
         'jg'      :  8,
         'loop'    :  9,
         'lcont'   : 10,
         'lbrk'    : 11,
         'push'    : 12,
         'pop'     : 13,
         'pop2'    : 14,
         'popn'    : 15,
         'pushfh'  : 16,
         'popth'   : 17,
         'movth'   : 18,
         'stkth'   : 19,
         'cpyh'    : 20,
         'seth'    : 21,
         'pshfhh'  : 22,
         'pshfhs'  : 23,
         'cmp'     : 24,
         'inc'     : 25,
         'dec'     : 26,
         'add'     : 27,
         'sub'     : 28,
         'mul'     : 29,
         'div'     : 30,
         'mod'     : 31,
         'nspct'   : 32,
	     'nspctst' : 33,
         'test_die': 34}


# Builds a dict that has the dict keys be the opcode instead of the mnemonic like opmap dict.
reversed_opmap = {value: key for key, value in opmap.items()}

def isInteger(x):
    try:
        int(x)
        return True
    except ValueError:
        return False
       
# build_prog() takes a string of raw pyasm text and returns a program list
# that is executable as is by the PVM.
def build_prog(text):
    in_comment = False # flag to tell tokenizer if it's looking at a comment.
    prog = [[0, 0]] # [0, 0] is prog metadata tag.
    label_map = {}  # dict to hold labels and their corresponding addresses.
    macro_map = {}
    tokenized_text = text.split() # split text up into tokens delimited by spaces.
    toknum = -1

    # iterate over token list one at a time processing them accordingly.
    while (toknum+1) < len(tokenized_text):
        toknum += 1
        tok = tokenized_text[toknum]

        # only process tokens if not in comment.
        if tok == '#' or tok[0] == '#' or tok[-1] == '#':
            if in_comment: # if we're in a comment already we've just found the end of it.
                in_comment = False
            else: # if not in comment we've found the start of one.
                in_comment = True
            continue
        if in_comment:
            continue

        # is token an instruction?
        if tok in opmap.keys():
            # found start of instruction so make new list and append to prog list.
            instr = []
            prog.append(instr)

            # append instruction opcode to instr list.
            instr.append(opmap[tok])

        # is token a value?
        elif isInteger(tok):
            instr.append(int(tok))

        # is token a macro declaration?
        elif tok == 'macro':
            # advance to next token which is the macro name.
            toknum += 1
            tok = tokenized_text[toknum]

            # check if macro name is already being used as a label name.
            if tok in label_map:
                raise Exception('invalid macro name, already used as label.')

            # advance to next token which is the macro's value.
            toknum += 1
            tok = tokenized_text[toknum]

            # make sure we actually have a valid integer.
            if not isInteger(tok):
                raise Exception('invalid macro value, not integer.')

            # everything's good, create our macro.
            macro_map[tokenized_text[toknum-1]] = int(tok)

        # is token a label declaration?
        elif tok[-1] == ':':
            # is it valid?
            if len(tok) > 1:
                # is label name an instr mnemonic and therefore invalid?
                if tok in opmap.keys():
                    raise Exception('label was instr mnemonic and therefore invalid.')
                 # label was instr mnemonic and therefore invalid

                # valid label so make entry for it. we're labelling the next instruction
                # so it's index within the prog list is the current prog list len plus 1.
                # cut off the ':' off end of the label.
                label_map[tok[:-1]] = len(prog)
            else:
                # label was too short.
                raise Exception('label too short')

        # is token an label identifier?
        elif tok in label_map.keys():
            instr.append(label_map[tok])

        # is token an macro identifier?
        elif tok in macro_map.keys():
            instr.append(macro_map[tok])

        # token isn't valid.
        else:
            print(tok)
            raise Exception('invalid token!\n')

    # program list is complete, update metadata tag list.
    try:
        # tells PVM where to begin execution.
        prog[0][0] = label_map['main']
    except KeyError:
        # main label missing.
        raise Exception('main label missing')

    # tells PVM program list size.
    prog[0][1] = len(prog)
    
    return prog

# takes path to .pal file and returns string of it.
def open_pal_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Error: The file was not found.")
    except PermissionError:
        print("Error: You do not have permission to access this file.")
    except IsADirectoryError:
        print("Error: The specified path is a directory, not a file.")
    except OSError as e:
        print(f"Error: An I/O error occurred. {e}")


def build_pvm_file(pvm_file_path, pal_file_path):
    # read pal file into text string.
    pal_text = open_pal_file(pal_file_path)

    # build program list.
    try:
        prog = build_prog(pal_text)

        with open(pvm_file_path, 'wb') as file:
            # Write the list to file.
            pickle.dump(prog, file)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except PermissionError:
        print("Error: You do not have permission to access this file.")
    except IsADirectoryError:
        print("Error: The specified path is a directory, not a file.")
    except OSError as e:
        print(f"Error: An I/O error occurred. {e}")
    except Exception as e:
        print(f"Error building program list: \n {e}")

def read_pvm_file(path):
    try:
        with open(path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except PermissionError:
        print("Error: You do not have permission to access this file.")
    except EOFError:
        print("Error: Reached end of file unexpectedly.")
    except pickle.UnpicklingError:
        print("Error: The file contains invalid pickle data.")
    except OSError as e:
        print(f"Error: An I/O error occurred. {e}")

# Takes a valid prog list, creates a string for each instruction
# then prints each instruction string one by one.
# these are in this format: [76] CALL 45 ([ADDR] MNEMONIC OPERAND1 OPERAND2)
def inspect_prog(prog):
    # iterate through instr lists within prog.
    # for each instr we make a string then print it.

    # prog[0] list is the metadata tag so first print it before iterating through rest of prog.
    print('program_size: %d\nstart_address: %d\n' % (prog[0][1], prog[0][0]))

    for addr, instr in enumerate(prog[1:]):
        # append instr address and mnemonic to instr string.
        instr_str = '[%d] %s' % (addr+1, reversed_opmap[instr[0]])

        # if instr length is more than one then iterate through the operands.
        if len(instr) > 1:
            for i in instr[1:]:
                # append operand value to instr string.
                instr_str += ' %d' % i

        # print completed instruction string.
        print(instr_str)

def assembler_tester(path_in):
    build_pvm_file('call_test.pvm', path_in)
    prog = read_pvm_file('call_test.pvm')
    print(prog)
    inspect_prog(prog)

def main():
    assembler_tester('call_test.pal')

#main()
