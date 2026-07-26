def iter_descendants(root):
    for row in range(root.rowCount()):
        node = root.child(row)
        yield node
        yield from iter_descendants(node)


def append_nodes_by_level(root, nodes):
    last_level = 0
    parents = []
    last_node = root

    for node in nodes:
        if node.level == last_level:
            parents[-1].appendRow(node)
        elif node.level > last_level:
            parents.append(last_node)
            parents[-1].appendRow(node)
        else:
            level_difference = last_level - node.level
            for _ in range(level_difference):
                parents.pop()
            parents[-1].appendRow(node)

        last_level = int(node.level)
        last_node = node
