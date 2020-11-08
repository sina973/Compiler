# #################### Scanner ###############################################
# Amirhossein Koochari 95170651
# Sina Radpour 97071002

class Node:

    def __init__(self, id):
        self.id = id
        self.exit_edge = {}
        self.back_track = False
        self.final_state = False
        self.description = ""

    def add_to_edges(self, node_id, expression):
        self.exit_edge[node_id] = expression

    def get_edges(self):
        return self.exit_edge

    def get_name(self):
        return self.id

    def set_back_track(self):
        self.back_track = True

    def set_final_state(self):
        self.final_state = True

    def set_description(self, description):
        self.description = description


Nodes = []
state = 0
keyword_list = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return']
symbol_list = []
for i in keyword_list:
    symbol_list.append([i])

errors = []
# open the input file
file = open("input.txt", 'r')
input_file = file.read()
file.close()
input_file += "$"
# print(input_file)
# open the error file
error_file = open("lexical_errors.txt", 'a')

# open the Symbol table file
symbol_table_file = open('symbol_table.txt', 'w')
symbol_table_file.write("1.\tif\n2.\telse\n3.\tvoid\n4.\tint\n5.\twhile\n6.\tbreak\n7.\tswitch\n8.\tdefault\n9.\tcase"
                        "\n10.\treturn\n")
# open the tokens file
tokens_file = open('tokens.txt', 'w')

while_state = True
pointer = 0
line = 1
tokens = []


for i in range(0, 16):
    Nodes.append(Node(i))

# #############  Add exit edges of each node ##################

Nodes[0].add_to_edges(1, ["letter"])
Nodes[0].add_to_edges(3, ["digit"])
Nodes[0].add_to_edges(5, [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<'])
Nodes[0].add_to_edges(6, ['='])
Nodes[0].add_to_edges(8, ['*'])
Nodes[0].add_to_edges(10, ['/'])
Nodes[0].add_to_edges(15, ['space'])
Nodes[0].add_to_edges(-1, ["$"])

Nodes[1].add_to_edges(1, ['letter', 'digit'])
Nodes[1].add_to_edges(2, ['other'])

Nodes[2].set_back_track()
Nodes[2].set_final_state()

Nodes[3].add_to_edges(4, ['other'])

Nodes[4].set_back_track()
Nodes[4].set_final_state()
Nodes[4].set_description("NUM")

Nodes[5].set_final_state()
Nodes[5].set_description("SYMBOL")

Nodes[6].add_to_edges(7, ['='])
Nodes[6].add_to_edges(9, ['other1'])

Nodes[7].set_final_state()
Nodes[7].set_description("SYMBOL")

Nodes[8].add_to_edges(9, ['other2'])

Nodes[9].set_back_track()
Nodes[9].set_final_state()
Nodes[9].set_description("SYMBOL")

Nodes[10].add_to_edges(11, ['/'])
Nodes[10].add_to_edges(13, ['*'])

Nodes[11].add_to_edges(12, ['\n'])
Nodes[11].add_to_edges(11, ['other3'])

Nodes[12].set_final_state()

Nodes[13].add_to_edges(13, ['other4'])
Nodes[13].add_to_edges(14, ['*'])

Nodes[14].add_to_edges(14, ['*'])
Nodes[14].add_to_edges(15, ['/'])
Nodes[14].add_to_edges(13, ['other5'])

Nodes[15].set_final_state()

# ###################### end of assignments ##########################

def is_valid(ch):           # Check if input character is valid
    valid_list = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<', '*', '=', '/', "$"]
    if ch.isdigit():
        return True
    if ch.isalpha():
        return True
    if ch.isspace():
        return True
    for i in range(0, len(valid_list)):
        if ch == valid_list[i]:
            return True

    return False

######################### On Edges Others function ######################

def is_other(ch):
    if not ch.isdigit():
        if not ch.isalpha():
            return True
    elif not ch.isalpha():
        return True
    return False

def is_other1(ch):
    if ch != "=":
        return True
    return False


def is_other2(ch):
    if ch != "/":
        return True
    return False


def is_other3(ch):
    if ch != "\n":
        return True
    return False


def is_other4(ch):
    if ch != "*":
        return True
    return False


def is_other5(ch):
    if ch != "*":
        if ch != '/':
            return True
    elif ch != "/":
        return True
    return False

# ################################# Error Handler ################################


def error_handler(error, lexeme, line):
    global errors
    errors.append([line, lexeme, error])


def error_description(s):
    if s == 8:
        return unmatched_comment_error()
    elif s == 3:
        return invalid_number_error()
    else:
        return unclosed_comment_error()


def unclosed_comment_error():
    return "Unclosed comment"


def unmatched_comment_error():
    return "Unmatched comment"


def invalid_number_error():
    return "Invalid number"

# ################################ End Of Error Handler ###############################

def check_edges(ch, state):
    global Nodes
    state_edges = Nodes[state].get_edges()
    return_state = False
    for k, v in state_edges.items():
        for i in v:
            if i == 'letter':
                if ch.isalpha():
                    return_state = k
            elif i == 'digit':
                if ch.isdigit():
                    return_state = k
            elif i == 'space':
                if ch.isspace():
                    return_state = k
            elif i == 'other':
                if is_other(ch):
                    return_state = k
            elif i == 'other1':
                if is_other1(ch):
                    return_state = k
            elif i == 'other2':
                if is_other2(ch):
                    return_state = k
            elif i == 'other3':
                if is_other3(ch):
                    return_state = k
            elif i == 'other4':
                if is_other4(ch):
                    return_state = k
            elif i == 'other5':
                if is_other5(ch):
                    return_state = k
            else:
                if ch == i:
                    return_state = k

    return return_state


def change_state_by_char(string, pointer, state, lexeme):
    global Nodes
    current_char = string[pointer]
    next_state = 0
    pointer_move = 0
    token_found = False
    error = ""
    temp_lexeme = ""
    if is_valid(current_char):
        next_state = check_edges(current_char, state)
        # print(next_state)
        if not next_state:
            error = error_description(state)
            pointer_move = 1
            temp_lexeme = lexeme + current_char
        else:
            # ################ change state
            if Nodes[next_state].final_state:
                token_found = True
                if Nodes[next_state].back_track:
                    temp_lexeme = lexeme
                    pointer_move = 0
                else:
                    temp_lexeme = lexeme + current_char
                    pointer_move = 1
            else:
                temp_lexeme = lexeme + current_char
                pointer_move = 1
    else:
        error = "invalid input"
        pointer_move = 1
        temp_lexeme = lexeme + current_char

    return token_found, next_state, pointer_move, temp_lexeme, error


def get_token_name(state, lexeme):
    if state == 2:
        for i in keyword_list[:11]:
            if lexeme == i :
                return "KEYWORD"
        return "ID"
    else:
        return Nodes[state].description


def get_next_token():
    global pointer
    global line
    global state
    global input_file
    global symbol_list
    temp_lexeme = ""
    token_name = ""
    return_state = []

    while True:
        #print(pointer, input_file[pointer], state)
        return_state = change_state_by_char(input_file, pointer, state, temp_lexeme)
        temp_lexeme = return_state[3]
        pointer += return_state[2]
        if return_state[0]:
            state = 0
            token_name = get_token_name(return_state[1], temp_lexeme)

            if return_state[1] == -1:
                return "(EOF, $)"

            if return_state[1] == 15:
                if pointer >= len(input_file):
                    #print("end of file")
                    return None
                if temp_lexeme == "\n":
                    # print("enter")
                    line += 1
                    # print(line)
                temp_lexeme = ""
            elif return_state[1] == 12:
                temp_lexeme = ""
            else:
                if token_name == "ID":
                    if temp_lexeme not in symbol_list:
                        symbol_list.append(temp_lexeme)
                return "(%s, %s)" % (token_name, temp_lexeme)
        elif return_state[4] != "":
            error_handler(return_state[4], temp_lexeme, line)
            temp_lexeme = ""
            state = 0
        else:
            state = return_state[1]

        if pointer >= len(input_file):
            if (state > 9 and state < 12) or (state > 12 and state < 15):
                error_handler("Unclosed Comment", "", line)
                state = 0
                return "(EOF, $)"

# ######################################### Parser #########################################################

def make_table(file_name):
    file = open(file_name, 'r')
    input_file_lines = file.readlines()
    file.close()

    table = {}

    terminals = []
    first_line = input_file_lines[0].split()
    for i in range(0, len(first_line)):
        terminals.append(first_line[i])

    for i in range(1, len(input_file_lines)):
        line = input_file_lines[i]
        words = line.split()
        temp_dictionary = {}
        for j in range(1, len(words)):
            temp_dictionary.update({terminals[j]: words[j].split("`")})
        table.update({words[0]: temp_dictionary})

    return table


def extract_token(temp_token):
    current_token = ""
    if temp_token[1:4] == "NUM":
        current_token = "num"
    elif temp_token[1:3] == "ID":
        current_token = "id"
    else:
        current_token = temp_token.split(",")[1]
        current_token = current_token[1:len(current_token)-1]
    return current_token


def is_terminal(stack_element):
    return not stack_element[0].isupper()


def add_error(error_number, token=None, top_stack=None):
    global parser_errors
    if error_number == 1:
        parser_errors.append("Misplaced %s, parser is skipping it" % token)
    elif error_number == 2:
        parser_errors.append("Missing term, pop %s from parser stack" % top_stack)
    elif error_number == 3:
        parser_errors.append("Inserting %s before %s, pop %s from parser stack" % (top_stack, token, top_stack))


def parser_check(stack_top, token):
    global parser_stack
    stack_terminal = is_terminal(stack_top)
    print("is terminal:", stack_terminal)
    if stack_terminal:
        if stack_top != token:
            parser_stack.pop()
            add_error(3, token, stack_top)
            return False
        else:
            parser_stack.pop()
            return True
    relation = tables.get(stack_top).get(token)
    print("relation:", relation)
    if len(relation) == 1:
        if relation[0] == ".":
            add_error(1, token)
            return True
        elif relation[0] == "synch":
            parser_stack.pop()
            add_error(2, token, stack_top)
            return False
        elif relation[0] == "e":
            parser_stack.pop()
            return False
        else:
            parser_stack.pop()
            parser_stack.append(relation[0])
            return False
    else:
        parser_stack.pop()
        for k in range(len(relation) - 1, -1, -1):
            parser_stack.append(relation[k])

        return False


tables = make_table("Parse Table.txt")
parser_stack = ["Program"]
parser_errors = []
current_token = ""

# for k in tables:
#     print("%s: " % k, end="")
#     print(tables.get(k))

get_token = True

while while_state:
    if get_token:
        current_temp_token = get_next_token()
        print("token:", current_temp_token)
        current_token = extract_token(current_temp_token)
        if len(tokens) < line:
            if current_temp_token:
                tokens.append([current_temp_token])
        else:
            if current_temp_token:
                tokens[line - 1].append(current_temp_token)
        if pointer >= (len(input_file)):
            while_state = False

    print("curent token:", current_token)
    print(parser_stack, "next is parser check !!!!!!!!!!!!!!!!!!!!!!!")
    get_token = parser_check(parser_stack[len(parser_stack) - 1], current_token)
    print("parser stack after check:", parser_stack)
    print("getting next token:", get_token)

    if len(parser_stack) < 1:
        while_state = False





