class Node:

    def __init__(self, id):
        self.id = id
        self.exit_edge = {}

    def add_to_edges(self, node, expression):
        self.exit_edge[node] = expression

    def get_edges(self):
        return self.exit_edge

    def get_name(self):
        return self.id


Nodes = {}
for i in range(0, 16):
    Nodes[i] = Node(i)


