from enum import Enum
from typing import Optional

class NodeColor(Enum):
    RED = 1
    BLACK = 2

    def __str__(self) -> str:
        if self == NodeColor.RED:
            return 'red'

        return 'black'

class NodePosition(Enum):
    Left = 1
    Right = 2
    Root = 3

    def __str__(self) -> str:
        if self == NodePosition.Left:
            return 'left'
        elif self == NodePosition.Right:
            return 'right'

        return 'root'

class Node:
    key: int
    data: any
    parent: Optional['Node'] = None
    right: Optional['Node'] = None
    left: Optional['Node'] = None
    color: NodeColor

    def __init__(
            self,
            key: int,
            data: any,
            parent: Optional['Node'] = None,
            color: NodeColor = NodeColor.RED,
    ):
        self.key = key
        self.data = data
        self.color = color
        self.parent = parent

    def grandparent(self) -> Optional['Node']:
        if self.parent is None:
            return None
        return self.parent.parent

    def brother(self) -> Optional['Node']:
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self) -> Optional['Node']:
        if self.parent is None:
            return None
        return self.parent.brother()

    def is_root(self) -> bool:
        return self.parent is None

    def position_in_parent_subtree(self) -> NodePosition:
        if self.parent is None:
            return NodePosition.Root

        if self == self.parent.left:
            return NodePosition.Left

        return NodePosition.Right

class RedBlackTree:
    root: Optional['Node'] = None

    def __str__(self):
        if self.root:
            return self.__tree_print(self.root, 'root:' + str(self.root.color) + ':')
        return 'Tree is empty'

    def __tree_print(
            self,
            node,
            prefix: str = '',
            child_prefix: str = ''
    ) -> str:
        if node is None:
            return ''

        result = prefix + str(node.key) + '\n'

        if node.right:
            result += self.__tree_print(node.right, child_prefix + '|-- r:' + str(node.right.color) + ':' + str(node.key) + ':', child_prefix + '|   ')
            result += child_prefix + '|\n'

        if node.left:
            result += child_prefix + '|\n'
            result += self.__tree_print(node.left, child_prefix + '|__ l:' + str(node.left.color) + ':' + str(node.key) + ':', child_prefix + '    ')

        return result

    def get(self, key: int) -> Optional[Node]:
        current = self.root

        while current is not None:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current

        return None

    def add(self, key: int, data: any):
        if self.root is None:
            self.root = Node(key, data, None, NodeColor.BLACK)
            return self.root

        current_node = self.root

        while current_node:
            if key == current_node.key:
                current_node.data = data
                break

            if key < current_node.key:
                if current_node.left is None:
                    current_node.left = Node(key, data, current_node)
                    self.__balance_after_add(current_node.left)
                    break

                current_node = current_node.left
            elif key > current_node.key:
                if current_node.right is None:
                    current_node.right = Node(key, data, current_node)
                    self.__balance_after_add(current_node.right)
                    break

                current_node = current_node.right

    def __rotate_to_left(self, node: Node) -> None:
        if node.parent is None:
            raise Exception('Leaf does not have a parent whose place it wants to take')

        old_root = node.parent
        new_root = node
        new_root_old_left_node = new_root.left

        self.__update_parent_link(old_root, new_root)

        new_root.left = old_root
        new_root.parent, old_root.parent = old_root.parent, new_root

        old_root.right = new_root_old_left_node

        if new_root_old_left_node:
            new_root_old_left_node.parent = old_root

    def __rotate_to_right(self, node: Node) -> None:
        if node.parent is None:
            raise Exception('Leaf does not have a parent whose place it wants to take')

        old_root = node.parent
        new_root = node
        new_root_old_right_node = new_root.right

        self.__update_parent_link(old_root, new_root)

        new_root.right = old_root
        new_root.parent, old_root.parent = old_root.parent, new_root

        old_root.left = new_root_old_right_node

        if new_root_old_right_node:
            new_root_old_right_node.parent = old_root

    def __update_parent_link(self, old_root: Node, new_root: Optional['Node']) -> None:
        match old_root.position_in_parent_subtree():
            case NodePosition.Root:
                self.root = new_root
            case NodePosition.Left:
                old_root.parent.left = new_root
            case NodePosition.Right:
                old_root.parent.right = new_root

    def __red_uncle(self, node: Node) -> None:
        node.parent.color = NodeColor.BLACK
        node.uncle().color = NodeColor.BLACK

        node.grandparent().color = NodeColor.RED

    def __black_uncle(self, node: Node) -> None:
        if node.grandparent().left == node.parent:
            if node.parent.right == node:
                self.__black_uncle_big_rotation_to_right(node)
            else:
                self.__black_uncle_rotation_to_right(node)

        elif node.grandparent().right == node.parent:
            if node.parent.left == node:
                self.__black_uncle_big_rotation_to_left(node)
            else:
                self.__black_uncle_rotation_to_left(node)

    def __black_uncle_big_rotation_to_right(self, node: Node) -> None:
        self.__rotate_to_left(node)
        self.__black_uncle_recolor(node.left)

        self.__rotate_to_right(node)

    def __black_uncle_big_rotation_to_left(self, node: Node) -> None:
        self.__rotate_to_right(node)
        self.__black_uncle_recolor(node.right)

        self.__rotate_to_left(node)

    def __black_uncle_rotation_to_right(self, node: Node) -> None:
        self.__black_uncle_recolor(node)
        self.__rotate_to_right(node.parent)

    def __black_uncle_rotation_to_left(self, node: Node) -> None:
        self.__black_uncle_recolor(node)
        self.__rotate_to_left(node.parent)

    def __black_uncle_recolor(self, node: Node) -> None:
        node.parent.color = NodeColor.BLACK
        node.grandparent().color = NodeColor.RED

    def __balance_after_add(self, node: Node) -> None:
        if node.is_root():
            node.color = NodeColor.BLACK

        elif node.color != NodeColor.BLACK and node.parent.color != NodeColor.BLACK:
            uncle = node.uncle()

            if uncle is not None and uncle.color == NodeColor.RED:
                self.__red_uncle(node)
            else:
                self.__black_uncle(node)

        if node.parent:
            self.__balance_after_add(node.parent)

    def __get_most_suitable_replacement_node(self, node: Node) -> Optional[Node]:
        if node.left is None and node.right is None:
            return None

        if node.left is None:
            return node.right

        if node.right is None:
            return node.left

        replacement_nodes = [
            self.__get_min_node(node.right),
            self.__get_max_node(node.left),
        ]

        for replacement_node in replacement_nodes:
            if replacement_node.color == NodeColor.RED:
                return replacement_node

        return replacement_nodes.pop()

    def __get_min_node(self, node: Node) -> Optional[Node]:
        current = node

        while current.left:
            current = current.left

        return current

    def __get_max_node(self, node: Node) -> Optional[Node]:
        current = node

        while current.right:
            current = current.right

        return current

    def delete(self, key: int) -> None:
        node_to_delete = self.get(key)
        if node_to_delete is None:
            raise Exception(f"Sheet with the key {key} is not in the tree.")

        suitable_node = self.__get_most_suitable_replacement_node(node_to_delete)

        if suitable_node:
            node_to_delete.key, suitable_node.key = suitable_node.key, node_to_delete.key
            node_to_delete.data, suitable_node.data = suitable_node.data, node_to_delete.data
            node_to_delete = suitable_node

        child = node_to_delete.left or node_to_delete.right

        if child:
            self.__replace_node(node_to_delete, child)
            child.color = node_to_delete.color
        else:
            if node_to_delete.is_root():
                self.root = None
            else:
                if node_to_delete.color == NodeColor.BLACK:
                    self.__balance_before_delete(node_to_delete)
                self.__replace_node(node_to_delete, None)

    def __replace_node(self, node: Node, child: Optional[Node]) -> None:
        self.__update_parent_link(node, child)
        if child:
            child.parent = node.parent

    def __balance_before_delete(self, node):
        while node != self.root and node.color == NodeColor.BLACK:
            if node == node.parent.left:
                brother = node.parent.right
                if brother.color == NodeColor.RED:
                    brother.color = NodeColor.BLACK
                    node.parent.color = NodeColor.RED
                    self.__rotate_to_left(brother)
                    brother = node.parent.right

                if (brother.left is None or brother.left.color == NodeColor.BLACK) and \
                        (brother.right is None or brother.right.color == NodeColor.BLACK):
                    brother.color = NodeColor.RED
                    node = node.parent
                else:
                    if brother.right is None or brother.right.color == NodeColor.BLACK:
                        if brother.left:
                            brother.left.color = NodeColor.BLACK
                        brother.color = NodeColor.RED
                        self.__rotate_to_right(brother.left)
                        brother = node.parent.right

                    brother.color = node.parent.color
                    node.parent.color = NodeColor.BLACK
                    if brother.right:
                        brother.right.color = NodeColor.BLACK
                    self.__rotate_to_left(brother)
                    node = self.root
            else:
                brother = node.parent.left
                if brother.color == NodeColor.RED:
                    brother.color = NodeColor.BLACK
                    node.parent.color = NodeColor.RED
                    self.__rotate_to_right(brother)
                    brother = node.parent.left

                if (brother.left is None or brother.left.color == NodeColor.BLACK) and \
                        (brother.right is None or brother.right.color == NodeColor.BLACK):
                    brother.color = NodeColor.RED
                    node = node.parent
                else:
                    if brother.left is None or brother.left.color == NodeColor.BLACK:
                        if brother.right:
                            brother.right.color = NodeColor.BLACK
                        brother.color = NodeColor.RED
                        self.__rotate_to_left(brother.right)
                        brother = node.parent.left

                    brother.color = node.parent.color
                    node.parent.color = NodeColor.BLACK
                    if brother.left:
                        brother.left.color = NodeColor.BLACK
                    self.__rotate_to_right(brother)
                    node = self.root

        node.color = NodeColor.BLACK

# tree = RedBlackTree()
#
# tree.add(6, 'ЕЕЕЕ')
# tree.add(20, 'ЕЕЕЕ')
# tree.add(60, 'ЕЕЕЕ')
# tree.add(8, 'ЕЕЕЕ')
# tree.add(7, 'ЕЕЕЕ')
# tree.add(27, 'ЕЕЕЕ')
# tree.add(96, 'ЕЕЕЕ')
# tree.add(23, 'ЕЕЕЕ')
# tree.add(53, 'ЕЕЕЕ')
# tree.add(52, 'ЕЕЕЕ')
# tree.add(54, 'ЕЕЕЕ')
# tree.add(55, 'ЕЕЕЕ')
# tree.add(56, 'ЕЕЕЕ')
# tree.add(72, 'ЕЕЕЕ')
# tree.add(2, 'ЕЕЕЕ')
# tree.add(5, 'ЕЕЕЕ')
#
# tree.delete(27)
# tree.delete(23)
# tree.delete(20)
# tree.delete(8)
# tree.delete(7)
# tree.delete(53)
# tree.delete(54)
# tree.delete(52)
# tree.delete(6)
# tree.delete(5)
# tree.delete(60)
# tree.delete(72)
# tree.delete(56)
# tree.delete(55)
# tree.delete(2)
# tree.delete(96)

# print(tree)