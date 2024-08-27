import compiler
import pickle

TEST_PYS_FILE = 'c:/Users/klopp/OneDrive/Desktop/pyson/ch.pys'
TEST_FILE_DUMP = 'tokenizer_test_dump.b'

# list of test-file token source strings in order.
token_string_map = [
    'sub', 'dickhole', '(', 'x', ',', 'y', ',', 'u', ')', '{', '}', 'sub', 'main', '(', 'main_var', ',', 'x', ')',
    '{', 'var', 'main_var2', '=', '5', 'const', 'Cc_var', '=', '67', 'if', '(', 'main_var', '==', '1', ')', '{', 'print',
    '(', 'main_var', ')', '}', 'elif', '(', 'cC_var', '!=', '68', ')', '{', 'print', '(', 'main_var', ')', '}', 'elif',
    '(', 'main_var', '<', '1', ')', '{', 'print', '(', 'main_var', ')', '}', 'elif', '(', 'cC_var', '>', '68', ')', '{',
    'print', '(', 'main_var', ')', '}', 'elif', '(', 'cC_var', '<=', '70', ')', '{', 'print', '(', 'main_var', ')', '}',
    'elif', '(', 'cC_var', '>=', '680', ')', '{', 'print', '(', 'main_var', ')', '}', 'else', '{', 'print', '(', 'main_var',
    ')', '}', 'if', '(', 'main_var', '==', '1', ')', '{', 'print', '(', 'main_var', ')', '}', 'elif', '(', 'cC_var', '!=',
    '68', ')', '{', 'print', '(', 'main_var', ')', '}', 'elif', '(', 'main_var', '<', '1', ')', '{', 'print', '(', 'main_var',
    ')', '}', 'elif', '(', 'cC_var', '>', '68', ')', '{', 'print', '(', 'main_var', ')', '}', 'elif', '(', 'cC_var', '<=',
    '70', ')', '{', 'print', '(', 'main_var', ')', '}', 'elif', '(', 'cC_var', '>=', '680', ')', '{', 'print', '(', 'main_var',
    ')', '}', 'else', '{', 'print', '(', 'main_var', ')', '}', 'while', '(', '!', 'x', ')', '{', 'fileopen', 'fileclose', '}',
    'x', '=', '[', '3', ',', '4', ',', '5', ',', '6', ']', 'y', '=', '&', 'x', 'while', '(', '!', 'x', ')', '{', 'fileopen',
    'fileclose', '}', 'x', '=', '[', '3', ',', '4', ',', '5', ',', '6', ']', 'y', '=', '&', 'x', 'return', 'x']

# list of test-file token codes in order.
test_token_codes = [
    2, 32, 11, 32, 34, 32, 34, 32, 12, 13, 14, 2, 32, 11, 32, 34, 32, 12, 13, 1, 32, 20, 33, 0, 32, 20, 33, 3, 11, 32, 24,
    33, 12, 13, 8, 11, 32, 12, 14, 4, 11, 32, 25, 33, 12, 13, 8, 11, 32, 12, 14, 4, 11, 32, 26, 33, 12, 13, 8, 11, 32, 12,
    14, 4, 11, 32, 27, 33, 12, 13, 8, 11, 32, 12, 14, 4, 11, 32, 28, 33, 12, 13, 8, 11, 32, 12, 14, 4, 11, 32, 29, 33, 12,
    13, 8, 11, 32, 12, 14, 5, 13, 8, 11, 32, 12, 14, 3, 11, 32, 24, 33, 12, 13, 8, 11, 32, 12, 14, 4, 11, 32, 25, 33, 12,
    13, 8, 11, 32, 12, 14, 4, 11, 32, 26, 33, 12, 13, 8, 11, 32, 12, 14, 4, 11, 32, 27, 33, 12, 13, 8, 11, 32, 12, 14, 4,
    11, 32, 28, 33, 12, 13, 8, 11, 32, 12, 14, 4, 11, 32, 29, 33, 12, 13, 8, 11, 32, 12, 14, 5, 13, 8, 11, 32, 12, 14, 6,
    11, 15, 32, 12, 13, 9, 10, 14, 32, 20, 30, 33, 34, 33, 34, 33, 34, 33, 31, 32, 20, 16, 32, 6, 11, 15, 32, 12, 13, 9, 10,
    14, 32, 20, 30, 33, 34, 33, 34, 33, 34, 33, 31, 32, 20, 16, 32, 7, 32]


def compiler_test():
    result = True
    token_list = []

    token_list = compiler.tokenize(TEST_PYS_FILE)
    # tokenize the test file.
    #try:
        #token_list = compiler.tokenize(TEST_PYS_FILE)
    #except Exception as e:
        #print('FAILED - tokenizer threw exception: %s' % e)
        #print('Tokens:')

        #if len(token_list):
        #    for token in token_list:
        #        token.print()

         #   return False

    # use token_list to produce a list of just the token codes.
    token_code_list = []
    for token in token_list:
        token_code_list.append(token.code)

    # check the token codes are correct.
    for token, code in zip(token_list, token_code_list):
        if token.code != code:
            result = False
            print('FAILED - token[%d] code is incorrect.')
            token.print_string()

    # check the token source strings are correct.
    # this confirms identifiers and integers are parsing correctly
    for token, string in zip(token_list, token_string_map):
        if token.string != string:
            result = False
            print('FAILED - token string %s len=%d doesn\'t match' % (token.string, len(token.string)))
            token.print()

    if result: print('compiler.tokenize() test passed!')

    # lets pickle the token list created for examination after.
    try:
        with open(TEST_FILE_DUMP, 'wb') as file:
            # Write the list to file.
            pickle.dump(token_list, file)
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

    return result

def main():
    compiler_test()

main()