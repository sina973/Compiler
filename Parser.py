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
    if temp_token[0] == "NUM":
        current_token = "num"
    elif temp_token[0] == "ID":
        current_token = "id"
    else:
        current_token = temp_token[1]
    return current_token


def is_terminal(stack_element):
    return stack_element[0].isupper()


def add_error(error_number, token=None, top_stack=None):
    global parser_errors
    if error_number == 1:
        parser_errors.apppend("Misplaced %s, parser is skipping it" % token)
    elif error_number == 2:
        parser_errors.apppend("Missing term, pop %s from parser stack" % top_stack)
    elif error_number == 3:
        parser_errors.apppend("Inserting %s before %s, pop %s from parser stack" % top_stack, token, top_stack)



def parser_check(stack_top, token):
    global parser_stack
    relation = tables.get(stack_top[0]).get(token)
    x = 0
    stack_terminal = is_terminal(stack_top[0])
    if stack_terminal:
        if stack_top[0] != token:
            add_error(3, token, stack_top[0])
    if len(relation) == 1:
        if relation[0] == ".":
            add_error(1, token)
        elif relation[0] == "synch":
            add_error(2, token, stack_top[0])
        elif relation[0] == "e":
            parser_stack.pop()
        else:
            parser_stack.pop()
            parser_stack.append(relation[0])
    else:
        while len(relation) != 0:
            parser_stack.append(relation.pop())


tables = make_table("Parse Table.txt")
parser_stack = ["Program"]
parser_errors = []

for k in tables:
    print("%s: " % k, end="")
    print(tables.get(k))

current_temp_token = ("", "")  # TODO: GET_NEXT_TOKEN should be implemented
current_token = extract_token(current_temp_token)






