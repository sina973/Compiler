class Node:

    def __init__(self, name, array=None):
        self.name = name
        self.exit_edge = array

    def add_to_edges(self, node, expression):
        self.exit_edge.append((node, expression))

    def get_edges(self):
        return self.exit_edge

    def get_name(self):
        return self.name


dictionary = {}
dictionary.