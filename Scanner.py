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
symbols = []
symbol_list = []
file = open("input.txt", 'r')
input_file = file.read()
file.close()
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

Nodes[1].add_to_edges(1, ['letter', 'digit'])
Nodes[1].add_to_edges(2, ['other'])

Nodes[2].set_back_track()
Nodes[2].set_final_state()

Nodes[3].add_to_edges(4, ['other_prime'])

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
Nodes[14].add_to_edges(13, ['other5'])

Nodes[15].set_final_state()

# ###################### end of assignments ##########################

def is_valid(ch):           # Check if input character is valid
    valid_list = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<', '*', '=', '/']
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

################################## Error Handler ################################

def error_handler(s):
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

################################# End Of Error Handler ###############################

def check_edges(ch, state):
    global Nodes
    state_edges =  Nodes[state].get_edges()
    return_state = False
    for k,v in state_edges:
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
        if not next_state:
            # Error handler(state)
        else:
            # ################ change state
            temp_lexeme = lexeme + current_char
            if Nodes[next_state].final_state:
                token_found = True
                if Nodes[next_state].back_track:
                    pointer_move = 0
                else:
                    pointer_move = 1
            else:
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
    temp_lexeme = ""
    token_name = ""
    return_state = []

    while True:
        return_state = change_state_by_char(input_file, pointer, state, temp_lexeme)
        temp_lexeme = return_state[3]
        pointer += return_state[2]
        if return_state[0]:
            state = 0
            token_name = get_token_name(return_state[1], temp_lexeme)
            if return_state[1] == 15:
                if temp_lexeme == "\n":
                    state = return_state[1]
                    line += 1
                temp_lexeme = ""
            elif return_state[1] == 12:
                temp_lexeme = ""
            else:
                return "(%s, %s)" % (token_name, temp_lexeme)


while while_state:
    get_next_token()
    if pointer == (len(input_file) - 1):
        while_state = False

