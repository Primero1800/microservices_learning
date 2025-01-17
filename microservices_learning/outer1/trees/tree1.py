class Node:
    def __init__(self, name):
        self.name = name
        self._left = None
        self._right = None

    def __repr__(self):
        return f"Node({self.name})"

    @property
    def right(self) -> 'Node':
        return self._right

    @right.setter
    def right(self, node):
        self._right = node

    @property
    def left(self) -> 'Node':
        return self._left

    @left.setter
    def left(self, node: 'Node'):
        self._left = node

    def has_left(self) -> bool:
        return self._left is not None

    def has_right(self) -> bool:
        return self._right is not None

def create_tree():
    n00 = Node('N00')
    n10 = Node('N10')
    n11 = Node('N11')

    n00.left = n10
    n00.right = n11

    n20 = Node('N20')
    n21 = Node('N21')
    n22 = Node('N22')
    n23 = Node('N23')

    n10.left = n20
    n10.right = n21
    n11.left = n22
    n11.right = n23

    return n00


def passing_right(root: Node) -> None:
    print("passing_right")
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.name, end=' ')
        if node.has_left():
            stack.append(node.left)
        if node.has_right():
           stack.append(node.right)
    print()


def passing_left(root: Node) -> None:
    print('Passing left')
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.name, end=' ')
        if node.has_right():
            stack.append(node.right)
        if node.has_left():
           stack.append(node.left)
    print()


def passing_top(root: Node) -> None:
    print('Passing top')
    stack = [root]
    while stack:
        node = stack.pop(0)
        print(node.name, end=' ')
        if node.has_left():
            stack.append(node.left)
        if node.has_right():
            stack.append(node.right)
    print()

def upping_from_left_bottom(root):
    print('Upping from left bottom')
    stack = [root]
    nodes = set()
    parents = {}

    while stack:
        node = stack.pop()
        nodes.add(node)
        if node.has_left():
            stack.append(node.left)
            parents[node.left.name] = node
        if node.has_right():
            stack.append(node.right)
            parents[node.right.name] = node
        start = node
    print({k:v.name for k, v in parents.items()})

    d = 2
    while nodes:
        node = start
        if node in nodes:
            print(node.name, end =' ')
            nodes.remove(node)

        if node.has_left() and node.left in nodes:
            start = node.left
        elif node.has_right() and node.right in nodes:
            start = node.right
        elif node.name in parents:
            start = parents[node.name]
        else:
            if nodes:
                raise Exception('Tree was modified while processing')

def _create_relatives(root):
    relatives = {}
    stack = [root]
    node = None

    while stack:

        node = stack.pop()
        if node not in  relatives:
            relatives[node] = {}

        if node.has_right():
            relatives[node]['right'] = node.right
            if node.right not in relatives:
                relatives[node.right] = {}
            relatives[node.right]['parent'] = node
            stack.append(node.right)

        if node.has_left():
            relatives[node]['left'] = node.left
            if node.left not in relatives:
                relatives[node.left] = {}
            relatives[node.left]['parent'] = node
            stack.append(node.left)

    print(relatives)
    return relatives, node

def rotate_right(root):
    print('Rotate right')
    relatives, new_root = _create_relatives(root)
    nodes = list(relatives)

    while nodes:
        node = nodes.pop()

        if 'right' in relatives[node]:
            relatives[node]['right'].left = node

        if 'left' in relatives[node]:
            node.right = relatives[node]['left']
            node.left = None

    passing_left(new_root)





if __name__ == "__main__":

    root = create_tree()

    passing_right(root)
    passing_left(root)
    passing_top(root)
    upping_from_left_bottom(root)

    print('********************')
    rotate_right(root)


