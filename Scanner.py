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
state = 'start'
lexeme = ''

for i in range(0, 16):
    Nodes[i] = Node(i)

# #############  Add exit edges of each node ##################

Nodes[0].add_to_edges(1, ["letter"])
Nodes[0].add_to_edges(3, ["digit"])
Nodes[0].add_to_edges(5, [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<'])
Nodes[0].add_to_edges(6, ['='])
Nodes[0].add_to_edges(8, ['*'])
Nodes[0].add_to_edges(10, ['/'])
Nodes[0].add_to_edges(15, ['space'])

Nodes[1].add_to_edges(1, ['letter', 'digit'])
Nodes[1].add_to_edges(2, ['other1'])
Nodes[1].add_to_edges(1, ['letter', 'digit'])
Nodes[1].add_to_edges(1, ['letter', 'digit'])








