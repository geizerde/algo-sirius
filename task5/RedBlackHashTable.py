from typing import Optional

from task4.RedBlackTree import RedBlackTree

class RedBlackHashTable:
    def __init__(self):
        self.tree = RedBlackTree()

    def put(self, key: any, value: any) -> None:
        self.tree.add(key.__hash__(), value)

    def get(self, key: any) -> Optional[any]:
        node = self.tree.get(key.__hash__())

        return node.data if node is not None else None

    def delete(self, key: any) -> None:
        self.tree.delete(key.__hash__())

ht = RedBlackHashTable()
ht.put("Anton1", 1)
ht.put("Anton2", 2)
ht.put("Anton3", 3)

print(ht.get("Anton1"))
print(ht.get("Anton2"))
print(ht.get("Anton3"))

ht.delete("Anton1")

print(ht.get("Anton1"))
