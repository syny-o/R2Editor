import re
from PyQt5.QtCore import Qt





def find_node_by_identifier(parent_node, identifier):
    FOUND_NODE = None

    for row in range(parent_node.rowCount()):            
        node = parent_node.child(row)
        if node.reference.lower() == identifier.lower():
            FOUND_NODE = node
            break

        FOUND_NODE = find_node_by_identifier(node, identifier)
        
        if FOUND_NODE:
            return FOUND_NODE
    
    return FOUND_NODE