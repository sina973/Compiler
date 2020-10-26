class Node:

    def __init__(self, id):
        self.id = id
        self.exit_edge = {}
        self.back_track = False
        self.final_state = False

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


Nodes = []
state = 0
lexeme = ''
symbol_list = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return']
file = open("input.txt", 'r')
input_file = file.read()
file.close()
while_state = True
pointer = 0
line = 0
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

Nodes[3].add_to_edges(4, ['other'])

Nodes[4].set_back_track()
Nodes[4].set_final_state()

Nodes[5].set_final_state()

Nodes[6].add_to_edges(7, ['='])
Nodes[6].add_to_edges(9, ['other1'])

Nodes[7].set_final_state()

Nodes[8].add_to_edges(9, ['other2'])

Nodes[9].set_back_track()
Nodes[9].set_final_state()

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


def check_edges(ch):
    state_edges =  Nodes[state].get_edges()
    for i in state_edges:




def get_next_token():
    temp_lexeme = ""
    current_char = input_file[pointer]
    if is_valid(current_char):
        check_edges(current_char)



while while_state:
    get_next_token()
    if pointer == (len(input_file) - 1):
        while_state = False
    pointer += 1
