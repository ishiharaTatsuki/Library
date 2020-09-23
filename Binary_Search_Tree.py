# O(logN)

class Node:
    def __init__(self, data):
        self.root = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.node = None

    def insert(self, data):
        if self.node is None:
            self.node = Node(data)
        else:
            self._insert(data, self.node)

    def _insert(self, data, cur_node):
        if data < cur_node.root:
            if cur_node.left is None:
                cur_node.left = Node(data)
            else:
                self._insert(data, cur_node.left)
        elif data > cur_node.root:
            if cur_node.right is None:
                cur_node.right = Node(data)
            else:
                self._insert(data, cur_node.right)
        else:
            print("同じ値があります。")

    def pre_order_print(self):
        if self.node:
            self._pre_order_print(self.node)

    def _pre_order_print(self, cur_node):
        if cur_node:
            print(" ", end="")
            print(cur_node.root, end="")
            self._pre_order_print(cur_node.left)
            self._pre_order_print(cur_node.right)

    def in_order_print(self):
        if self.node:
            self._in_order_print(self.node)

    def _in_order_print(self, cur_node):
        if cur_node:
            self._in_order_print(cur_node.left)
            print(" ", end="")
            print(cur_node.root, end="")
            self._in_order_print(cur_node.right)

    def find_rec(self, data):
        if self.node:
            is_found = self._find(data, self.node)
            if is_found:
                return True
            return False
        else:
            return None

    def _find(self, data, cur_node):
        if data > cur_node.root and cur_node.right:
            return self._find(data, cur_node.right)
        elif data < cur_node.root and cur_node.left:
            return self._find(data, cur_node.left)
        if data == cur_node.root:
            return True

    # 削除する場合の探索
    def find_min(self, cur_node=None):
        if self.node is None:
            return None
        while cur_node.left:
            cur_node = cur_node.left
        return cur_node

    def delete_node(self, data):
        if self.node is None:
            return False
        else:
            self.node = self._delete_node(data, self.node)

    def _delete_node(self, data, cur_node):
        if cur_node is None:
            return cur_node
        if data < cur_node.root:
            cur_node.left = self._delete_node(data, cur_node.left)
        elif data > cur_node.root:
            cur_node.right = self._delete_node(data, cur_node.right)
        else:
            # 子ノードが一つまたはなしの場合
            if cur_node.left is None:
                tmp = cur_node.right
                cur_node = None
                return tmp
            elif cur_node.right is None:
                tmp = cur_node.left
                cur_node.left = None
                return tmp
            # 子ノードが2つの場合は右側の一番小さい値
            tmp = self.find_min(cur_node.right)
            cur_node.root = tmp.root
            cur_node.right = self._delete_node(tmp.root, cur_node.right)
        return cur_node

    # 探索 ループ版 メソッド
    def find_by_while(self, data):
        if self.node is None:
            return None
        cur_node = self.node
        while cur_node:
            if data == cur_node.root:
                return True
            if data < cur_node.root:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
        return False

#-----------------------------
def resolve():
# 使用例
# inputdata :  insert, 20:(string, value)
    N = int(input())
    bst = BST()
    for line in range(N):
        s = input.split()

        if s[0] == "insert":
            x = int(s[1])
            bst.insert(x)
        elif s[0] == "find":
            x = int(s[1])
            if bst.find_rec(x):
                print("yes")
            else:
                print("no")
        elif s[0] == "delete":
            x = int(s[1])
            bst.delete_node(x)
        else:
            # 出力規定： 先頭に1つの空白もいれる
            bst.in_order_print()
            print()
            bst.pre_order_print()
            print()


if __name__ == '__main__':
    resolve()
