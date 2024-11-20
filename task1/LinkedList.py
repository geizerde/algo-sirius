class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def reverse(self):
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def delete(self, value):
        current = self.head
        prev = None

        if current and current.value == value:
            self.head = current.next
            return

        while current and current.value != value:
            prev = current
            current = current.next

        if not current:
            return

        prev.next = current.next

    def insert(self, value, position):
        new_node = Node(value)

        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        count = 0

        while current and count < position - 1:
            current = current.next
            count += 1

        if not current:
            print('Не правильно задана позиция')
            return

        new_node.next = current.next
        current.next = new_node

    def __print_list(self, node):
        print(node.data)
        if node.next is not None:
            self.__print_list(node.next)

    def print_list(self):
        if self.head is not None:
            self.__print_list(self.head)