class Node:

    def __init__(self, id):
        self.id = id
        self.exit_edge = {}
        self.back_track = False

    def add_to_edges(self, node, expression):
        self.exit_edge[node] = expression

    def get_edges(self):
        return self.exit_edge

    def get_name(self):
        return self.id

    def set_back_track(self):
        self.back_track = True


Nodes = {}
state = 'start'
for i in range(0, 16):
    Nodes[i] = Node(i)

Nodes[0].add_to_edges()


