import assembler
import pickle

ID_MAXLEN = 30

def pickle_token_list(token_list):
    TEMP_TOKEN_DUMPFILE = 'temp_token_dump.b'
    # dump token list to temp file.
    try:
        with open(TEMP_TOKEN_DUMPFILE, 'wb') as file:
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

# parent token type code list.
token_type_list = {
    'KEYWORD'    :  500,
    'IDENTIFIER' :  501,
    'INTEGER'    :  502,
    'OPERATOR'   :  503}

# keyword type code list.
# codes match their respective entries in mnemonic list.
keyword_list = {
    'const'      :  0,
    'var'        :  1,
    'sub'        :  2,
    'if'         :  3,
    'elif'       :  4,
    'else'       :  5,
    'while'      :  6,
    'return'     :  7,
    'print'      :  8,
    'fileopen'   :  9,
    'fileclose'  : 10}

# token mnemonic list.
# codes match their respective entries in mnemonic list.
token_mnemonic = {
    0  : "CONST_DEC",
    1  : "VAR_DEC",
    2  : "SUB_DEC",
    3  : "IF_STMT",
    4  : "ELIF_STMT",
    5  : "ELSE_STMT",
    6  : "WHILE_STMT",
    7  : "RETURN_STMT",
    8  : "PRINT_KEYWORD",
    9  : "FILEOPEN_KEYWORD",
    10 : "FILECLOSE_KEYWORD",
    11 : "L_PAREN",
    12 : "R_PAREN",
    13 : "L_CBRACE",
    14 : "R_CBRACE",
    15 : "L_BRACKET",
    16 : "R_BRACKET",
    17 : "NOT_OP",
    18 : "ADDR_OP",
    19 : "ADD_OP",
    20 : "SUB_OP",
    21 : "MUL_OP",
    22 : "DIV_OP",
    23 : "MOD_OP",
    24 : "ASSIGN_OP",
    25 : "IDENTIFIER",
    26 : "INTEGER",
    27 : "LT_OP",
    28 : "GT_OP",
    29 : "COMMA",
    30 : "EQ_OP",
    31 : "NOT_EQ_OP",
    32 : "LE_OP",
    33 : "GE_OP"}

# operator type code list.
operator_list = {
    '('  : 11,
    ')'  : 12,
    '{'  : 13,
    '}'  : 14,
    '['  : 15,
    ']'  : 16,
    '!'  : 17,
    '&'  : 18,
    '+'  : 19,
    '-'  : 20,
    '*'  : 21,
    '/'  : 22,
    '%'  : 23,
    '='  : 24,
    '<'  : 27,
    '>'  : 28,
    ','  : 29,
    '==' : 30,
    '!=' : 31,
    '<=' : 32,
    '>=' : 33}

class Token:
    def __init__(self, _type, subtype, line, col, rawstr, ndx, value=None):
        self.type = _type # master token type code.
        self.subtype = subtype # specifies what op, keyword ect token is.
        self.line = line # line token is on source file.
        self.col  = col # col token is on source file.
        self.rawstr = rawstr # raw string from source file, '+', 'sub', 'var_name' ect.
        self.value = value # used by integer tokens.
        self.mnemonic = token_mnemonic[subtype]
        self.ndx = ndx # position within token list.
        self.print_str = self.build_print_str() # metadata print string.

    def build_print_str(self):
        if self.type == 502:
            vs = 'value: <%d>' % self.value
        else:
            vs = ''

        return '<%s> @ col %d line %d raw-string: [%s] %s index: %d' % (self.mnemonic, self.col, self.line, self.rawstr, vs, self.ndx)

    def print(self):
        print(self.print_string)

class TokenList:
    def __init__(self):
        self.list = []

    def print_all(self):
        for token in self.list:
            token.print()

    def print_token(self, ndx):
        self.list[ndx].print()

    def create(self, _type, subtype, line, col, rawstr, value=None):
        self.list.append(Token(_type, subtype, line, col, rawstr, len(self.list) + 1, value))

# list of operators 1st chars, used by is_operator() for detecting operators.
op1stchars = ['(', ')', '{', '}', '[', ']', '!', '&', '+', '-', '*', '/', '%', '=', '<', '>', ',']

def is_operator(char):
    return char in op1stchars

# Determines if the passed char is an identifier or integer string delimiter.
def delimiter_reached(char, col, line_len):
    print('col=%d linelen=%d c=[%s]' % (col, line_len, char))
    if col > line_len:        return 1 # EOL.
    if char == '\n':          return 1 # EOL.
    if char == ' ':           return 2 # whitespace.
    if char == '#':           return 3 # comment.
    if is_operator(char):     return 4 # operator.
    return 0 # no delimiter.

def valid_id_char(char):
    return char.isalnum() or char == '_'


def tokenize(pys_file_path):
    toklist = TokenList()
    col_num = -1
    line_num = 0
    line_len = 0
    str_start_col = 0
    skip_line = False

    try:
        file = open(pys_file_path, 'r')
    except FileNotFoundError:
        print("The file \"%s\" does not exist." % pys_file_path)

    # iterate through source file lines one by one.
    for line in file:
        line_len = len(line) - 1
        line_num += 1
        col_num = -1
        print('LINE[%d]=[%s]LEN=%d' % (line_num, line, line_len))

        # skip empty lines.
        if line_len == 0:
            print('skipped empty line %d' % line_num)
            continue

        # char processing loop.
        # iterate through line's chars one by one, using while stmt because at times we must
        # look one or more chars ahead ect. to process next char just continue this while stmt.
        # when we are done with the line we just break from this while loop and the next cycle
        # of <for line in file> executes.
        while True:
            col_num += 1

            # for some mysterious reason this is how we must detect
            # the EOL of the last line in the file.
            if col_num > line_len: break

            # assign char we're processing to char variable.
            char = line[col_num]

            # deal with end of line, no idea why sometimes it's dealt with by the code below
            # yet sometimes dealt with <if col_num > line_len: break> code above.
            if char == '\n':
                print('EOL FOUND LINE[%d]' % line_num)
                break

            # handle our whitespace and comments. if char is whitespace process next char.
            if char == ' ':
                print('skipped whitespace char line %d col %d' % (line_num, col_num+1))
                continue

            # if char is comment the entire line is just skipped.
            if char == '#':
                print('skipped comment line %d' % line_num)
                break

            # are we dealing with an integer value?
            if char.isdigit():
                num_str = char # buffer used to build multi-digit numbers(integers).
                str_start_col = col_num - 1 # hold the col of mumber.

                # is it a single digit number? check if next char is a delimiter.
                # check if we've reached end of the integer by finding a
                # delimiter at the next char after this current one being processed.
                if delimiter_reached(line[col_num + 1], col_num, line_len):
                    # we have single digit int, create token then continue to next char.
                    toklist.create(502, 502, line_num, str_start_col, char, int(num_str))
                    continue

                # no delimiter found so we have multi-digit number, build it's string.
                while True:
                    col_num += 1
                    char = line[col_num]

                    # check if we have an invalid char for an integer value.
                    if not char.isdigit():
                        raise Exception('invalid integer [%s] on line: %d col: %d' % (num_str + char, line_num, col_num + 1))

                    # append to num string and continue building.
                    num_str += char

                    # check if we've reached end of the integer by finding a delimiter at the next 
                    # char after this current one.
                    if delimiter_reached(line[col_num + 1], col_num, line_len):
                        # integer complete, tokenize that slut.
                        toklist.create(502, 502, line_num, str_start_col, char, int(num_str))
                        break

                # finished processing integer so continue next iteration of char processing loop.
                continue

            # check for all possible single char tokens before processing identifers & keywords.
            # if found, create token and continue processing next char.
            if char == '(':
                toklist.create(503, 11, line_num, col_num, char)
                continue

            elif char == ')':
                toklist.create(503, 12, line_num, col_num, char)
                continue

            elif char == '{':
                toklist.create(503, 13, line_num, col_num, char)
                continue

            elif char == '}':
                toklist.create(503, 14, line_num, col_num, char)
                continue

            # '!' char could be not operator or first char of not-equal operator.
            # so we look ahead at next char to determine.
            elif char == '!':
                # determine if we have not-equal operator by looking ahead to next char
                # and checking if it is a '=' character.
                if line[col_num + 1] == '=':
                    toklist.create(503, 31, line_num, col_num, char)
                    # advance col_num past 2nd char of '!=' operator. so that next iteration of char 
                    # processing loop is looking at the correct char.
                    col_num += 1
                    continue

                # determine if next char is space, if so we have a not operator. 
                # create it's token then continue processing next char.
                elif char == ' ':
                    toklist.create(503, 17, line_num, col_num, char)
                    continue

            elif char == '&':
                toklist.create(503, 18, line_num, col_num, char)
                continue

            elif char == '*':
                toklist.create(503, 21, line_num, col_num, char)
                continue

            elif char == '-':
                toklist.create(503, 20, line_num, col_num, char)
                continue

            elif char == '+':
                toklist.create(503, 19, line_num, col_num, char)
                continue

            elif char == '%':
                toklist.create(503, 23, line_num, col_num, char)
                continue

            elif char == "/":
                toklist.create(503, 22, line_num, col_num, char)
                continue

            elif char == '=':
                # determine if we have equal operator by looking ahead to next char
                # and checking if it is a '=' character.
                if line[col_num + 1] == '=':
                    toklist.create(503, 30, line_num, col_num, char)
                    # advance col_num past 2nd char of '!=' operator. so that next iteration of char 
                    # processing loop is looking at the correct char.
                    col_num += 1
                    continue

                # determine if next char is space, if so we have an assignment operator.
                elif char == ' ':
                    toklist.create(503, 24, line_num, col_num, char)
                    continue

            elif char == '<':
                # determine if we have less-than-or-equal operator by looking ahead to next char
                # and checking if it is a '=' character.
                if line[col_num + 1] == '=':
                    toklist.create(503, 32, line_num, col_num, char)
                    # advance col_num past 2nd char of '!=' operator. so that next iteration of char 
                    # processing loop is looking at the correct char.
                    col_num += 1
                    continue

                # determine if next char is space, if so we have valid less-than operator.
                elif char == ' ':
                    toklist.create(503, 27, line_num, col_num, char)
                    continue

            elif char == '>':
                # determine if we have greater-than-or-equal operator by looking ahead to next char
                # and checking if it is a '=' character.
                if line[col_num + 1] == '=':
                    toklist.create(503, 33, line_num, col_num, char)
                    # advance col_num past 2nd char of '!=' operator. so that next iteration of char 
                    # processing loop is looking at the correct char.
                    col_num += 1
                    continue

                # determine if next char is space, if so we have valid greater-than operator.
                elif char == ' ':
                    toklist.create(503, 28, line_num, col_num, char)
                    continue

            elif char == '[':
                toklist.create(503, 15, line_num, col_num, char)
                continue

            elif char == ']':
                toklist.create(503, 16, line_num, col_num, char)
                continue

            elif char == ',':
                toklist.create(503, 29, line_num, col_num, char)
                continue

            # handle identifiers & keywords, check if char is valid starting character.
            if valid_id_char(char):
                print('found valid id char')
                # we have valid start to our identifier or keyword so lets build the string.
                str_start_col = col_num - 1
                string = char

                # string building loop.
                while True:
                    col_num += 1
                    char = line[col_num]

                    # check if char is identifier delimiter of some kind.
                    # if so break out of string building loop and tokenize it.
                    if delimiter_reached(line[col_num + 1], col_num, line_len):
                        print(delimiter_reached(line[col_num + 1], col_num, line_len))
                        print('delim reached [%s] <%s>' % (string, line[col_num + 1]))
                        break

                    # check if char is valid identifer char then add to string
                    if valid_id_char(char):
                        string += char
                    else:
                        raise Exception('invalid identifier char [%s] on line: %d col: %d' % (char, line_num, col_num + 1))

                # confirm the string is valid identifier or keyword before tokenization.
                # check if it exceeds the maximum identifier length.
                if len(string) > ID_MAXLEN:
                    raise Exception('invalid identifier [%s] exceeds maximum length on line: %d col: %d' % (string, line_num, col_num + 1))

                # is the string a keyword?
                if string in keyword_list.keys():
                    toklist.create(500, keyword_list[string], line_num, col_num, char)
                    break

                # string is valid identifier, tokenize it. then
                # continue processing next char in line
                toklist.create(501, 501, line_num, col_num, char)
                continue

    file.close() # close .pys file we just tokenized.

    return token_list


def main():
    print(1234)

#main()