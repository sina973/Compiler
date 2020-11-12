from anytree import *

udo = Node("UDO")
par = Node("pae", parent=udo)
par.parent
par.name = "XXX"
print(par)