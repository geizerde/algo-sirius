from typing import Optional

class Node:
    data: int
    right: Optional['Node'] = None
    left: Optional['Node'] = None

    def __init__(self, data: int):
        self.data = data

class BinarySearchTree:
    root: Optional['Node'] = None

    def __str__(self):
        return self.__tree_print(self.root)

    def __tree_print(
            self, node,
            prefix: str = '',
            child_prefix: str = ''
    ) -> str:
        if node is None:
            return ''

        result = prefix + str(node.data) + "\n"

        if node.right:
            result += self.__tree_print(node.right, child_prefix + "|-- r:", child_prefix + "|   ")
            result += child_prefix + "|\n"

        if node.left:
            result += child_prefix + "|\n"
            result += self.__tree_print(node.left, child_prefix + "|__ l:", child_prefix + "    ")

        return result

    def __height(self, node: Node):
        if node is None:
            return 0
        return max(self.__height(node.left), self.__height(node.right)) + 1

    def height(self) -> int:
        if self.root is None:
            return 0

        return self.__height(self.root)

    def __rotate_to_left(self, node: Node) -> Node:
        if node.right is None:
            raise Exception(
                'It is impossible to make a left turn because there is no node on the right that could become a new root of the subtree'
            )

        old_root = node
        new_root = node.right
        new_root_old_left_node = new_root.left

        new_root.left = old_root
        old_root.right = new_root_old_left_node

        return new_root

    def __rotate_to_right(self, node: Node) -> Node:
        if node.left is None:
            raise Exception(
                'It is impossible to make a right turn because there is no node on the left that could become a new root of the subtree'
            )

        old_root = node
        new_root = node.left
        new_root_old_right_node = new_root.right

        new_root.right = old_root
        old_root.left = new_root_old_right_node

        return new_root

    def __balance(self, node: Node) -> Optional[Node]:
        if node is None:
            return node

        node.left = self.__balance(node.left)
        height_left = self.__height(node.left)
        height_right = self.__height(node.right)

        if height_left - height_right > 1:
            if self.__height(node.left.right) > self.__height(node.left.left):
                node.left = self.__rotate_to_left(node.left)
            node = self.__rotate_to_right(node)

        node.right = self.__balance(node.right)
        height_left = self.__height(node.left)
        height_right = self.__height(node.right)

        if height_right - height_left > 1:
            if self.__height(node.right.left) > self.__height(node.right.right):
                node.right = self.__rotate_to_right(node.right)
            node = self.__rotate_to_left(node)

        return node

    def balance(self) -> None:
        if self.root is not None:
            self.root = self.__balance(self.root)

    def __delete(self, node: Node, elem: int) -> Optional[Node]:
        if node is None:
            return None

        if elem < node.data:
            node.left = self.__delete(node.left, elem)
        elif elem > node.data:
            node.right = self.__delete(node.right, elem)
        else:
            if node.left is None and node.right is None:
                return None

            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            min_right_node = self.__get_min_node(node.right)
            node.data = min_right_node.data

            node.right = self.__delete(node.right, min_right_node.data)

        return node

    def delete(self, elem: int) -> None:
        if self.root is None:
            return

        self.root = self.__balance(
            self.__delete(self.root, elem)
        )

    def __get_min_node(self, node: Node) -> Optional[Node]:
        current = node

        while current.left:
            current = current.left

        return current

    def add(self, data: int) -> None:
        if self.root is None:
            self.root = Node(data)
            return

        current_node = self.root

        while current_node:
            if data < current_node.data:
                if current_node.left is None:
                    current_node.left = Node(data)
                    break

                current_node = current_node.left
            elif data > current_node.data:
                if current_node.right is None:
                    current_node.right = Node(data)
                    break

                current_node = current_node.right

    def __invert(self, node: Node) -> Optional[Node]:
        if node is None:
            return None

        node.left, node.right = node.right, node.left

        self.__invert(node.left)
        self.__invert(node.right)

        return node

    def invert(self) -> None:
        self.root = self.__invert(self.root)

# tree = BinarySearchTree()
#
# tree.add(6)
# tree.add(20)
# tree.add(60)
# tree.add(8)
# tree.add(7)
# tree.add(27)
# tree.add(96)
# tree.add(23)
# tree.add(53)
# tree.add(52)
# tree.add(54)
# tree.add(55)
# tree.add(56)
# tree.add(72)
# tree.add(2)
# tree.add(5)


# tree.add(8)
# tree.add(7)
# tree.add(6)
# tree.add(5)
# tree.add(4)
# tree.add(3)
# tree.add(2)

# tree.add(6)
# tree.add(20)
# tree.add(60)
# tree.add(8)
#
# tree.delete(6)
# tree.delete(20)
# tree.delete(60)
# tree.delete(8)
#

# tree.balance()
# print(tree)