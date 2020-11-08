
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



tables = make_table("Parse Table.txt")
parser_stack = ["Program"]

for k in tables:
    print("%s: " % k, end="")
    print(tables.get(k))

current_temp_token = ("", "")  # TODO: GET_NEXT_TOKEN should be implemented
current_token = extract_token(current_temp_token)






