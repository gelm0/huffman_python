'''
Class for building a tree
'''
class Node:
    def __init__(self, symbol, freq):
        self._symbol = symbol
        self._freq = freq
        self._left_child = None
        self._right_child = None

    def __lt__(self, other):
        return self._freq < other._freq

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        if other is None:
            return False

        return (self._symbol == other._symbol) and (self._freq == other._freq)

    def __hash__(self):
        return hash((self._symbol, self._freq))
    
    def get_freq(self) -> int:
        return self._freq

    def set_childs(self, lchild, rchild) -> None:
        self._right_child = rchild
        self._left_child = lchild

    def get_symbol(self):
        return self._symbol

    def get_rchild(self):
        return self._right_child

    def get_lchild(self):
        return self._left_child
