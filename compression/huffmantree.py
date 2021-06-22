"""
Huffmantree implementation
"""
import heapq
from heapq import heapify
from bitarray import bitarray
from bitarray.util import zeros
from collections import Counter
from compression import node


class HuffmanInitException(Exception):
    '''
    Exception to be thrown when Huffman tree has not been initialized
    '''
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return f'Huffman tree has not been initialized properly.\
                {self._message}.'


class Util:
    '''
    Util class for shared components
    '''
    @staticmethod
    def bitwise_add(nbr1: bitarray, nbr2: bitarray) -> bitarray:
        '''
        Performs addition of two bitarrays
        '''
        while nbr2 != zeros(len(nbr2)):
            nbr1 = nbr1 ^ nbr2
            nbr2 = (nbr1 & nbr2) << 1
        return nbr1


class HuffmanTree:
    '''Class to create a huffman tree

    Constructs a huffman tree from either text or file input. The class
    consists of two main methods in order to do this

    1. get_symbol_tree(file_name: str, data: str)
    2. get_tree(file_name: str, data: str)

    The 1st method returns a sorted dictionary from shortest to longest
    huffmande code, of all symbols.

    The 2nd method returns a dictionary if all the nodes and their
    corresponding huffman codes. This can be useful in the instances
    that you want more information about the symbols, such as their
    respective frequencies.

    Parameters
    ---------
    print_tree: boolean, optional, default False
        Prints the whole huffman tree when it's being constructed with
        symbol, frequency, huffman code and if it's a leaf node
    file_name: str, optional
        Name of the file which content should be used to construct the
        huffman tree.
    data: str, optional
        Input string which should be used to construct the huffman tree.
    If both are supplied the file_name will take precident.

    Raises
    -----
    HuffmanInitException if neither file_name or data is supplied
    '''
    def __init__(self, print_tree: bool = False,
                 file_name: str = None, data: str = None):
        self._print_tree: bool = print_tree
        self._tree: dict = {}
        self.check_data_tree_init(file_name, data)

    def get_symbol_tree_by_val(self) -> dict:
        '''
        Returns a huffman tree dict. Needed for 'ordinary' huffman encoding
        ['symbol': bitarray(Huffman Code)]

        Returns
        ------
        A dictionary of key,values with types [str, bitarray] where the
        bitarray contains the corresponding huffman code for the symbol.
        '''

        return dict(sorted(dict(map(lambda node: (node[0].get_symbol(),
                                                  node[1]),
                    self._tree.items())).items(),
                    key=lambda val: val[1]))

    def get_symbol_tree_by_val_len(self) -> dict:
        '''
        Returns a huffman tree dict sorted by length of value.
        Needed for canonical huffman encoding['symbol': bitarray(Huffman Code)]

        Returns
        ------
        A dictionary of key,values with types [str, bitarray] where the
        bitarray contains the corresponding huffman code for the symbol.
        '''
        return dict(sorted(dict(map(lambda node: (node[0].get_symbol(),
                                                  node[1]),
                    self._tree.items())).items(),
                    key=lambda val: len(val[1])))

    def get_canon_tree(self) -> dict:
        '''
        Initializer function for canonical huffman tree
        '''
        canon_tree = {}
        symbol_tree = self.get_symbol_tree_by_val_len()
        first_sym = next(iter(symbol_tree.keys()))
        curr_len = len(symbol_tree[first_sym])
        # Remove first item as it has been set
        del symbol_tree[first_sym]
        code = canon_tree[first_sym] = zeros(curr_len)
        self.build_canon_dict(canon_tree, symbol_tree, code)
        return canon_tree

    def get_tree(self) -> dict:
        '''
        Returns a huffman tree dict. ['Node': bitarray(Huffman Code)]

        Returns
        ------
        A dictionary of key,values with types [Node, bitarray] where the
        bitarray contains the corresponding huffman code for the Node.
        '''
        return self._tree

    def check_data_tree_init(self, file_name: str, data: str) -> None:
        '''
        Initializes the huffman tree
        '''
        self.tree_init(file_name, data)
        if not self._tree:
            raise HuffmanInitException('Please supply data or file_name to '
                                       'initialize the huffman tree')

    def tree_init(self, file_name: str, data: str):
        '''
        Tries to initialize the huffman tree with from the file_name.
        If that isin't supplied tries with data instead.
        '''
        if file_name:
            self.build_tree_from_file(file_name)
        elif data:
            self.build_tree_from_data(data)

    def build_tree_from_file(self, file_name: str):
        '''
        Helper function to build huffman tree from file.
        See buld_tree_from_data for logic.
        '''
        with open(file_name, 'rb') as fin:
            self.build_tree_from_data(fin.read())

    def build_tree_from_data(self, data: str) -> None:
        '''
        Responsible for the build flow of the huffman tree.
        First creates a dictionary of all corresponding characters frequency
        in the supplied data. Then constructs a minheap with the lowest
        frequency node as root. Lastly the tree is traversed bottom-up to
        construct the huffman tree.

        Parameters
        ---------
        data: str
            The supplied content for which the huffman tree is created.
        '''
        char_freq = Counter(data)
        heap_list = self.heapify_freq(char_freq)
        root = self.build_huffman_tree(heap_list)
        self.build_tree_dict(root, '')

    def build_canon_dict(self, canon_tree: dict, symbol_tree: dict,
                         code: bitarray) -> None:
        '''
        Recursive function that builds the canonical huffman tree

        Parameters
        ---------
        canon_tree: dict
            The tree will be store in here with symbol as key and code as value
        symbol_tree: dict
            The constructed non-canonical huffman dict
        code: bitarray
            The current canonical huffman code
        '''
        if len(symbol_tree) == 0:
            return
        symbol = next(iter(symbol_tree.keys()))
        value = symbol_tree[symbol]
        del symbol_tree[symbol]
        curr_len = len(code)
        temp_len = len(value)
        next_code = code << 1
        next_code = Util.bitwise_add(code, zeros(len(code) - 1)
                                     + bitarray('1'))
        if temp_len > curr_len:
            # Pad with 1 after increment when length has shifted
            next_code += bitarray('1')
        canon_tree[symbol] = next_code
        self.build_canon_dict(canon_tree, symbol_tree, next_code)

    @classmethod
    def heapify_freq(cls, char_freq: dict) -> list:
        '''
        Constructs a min heap from a dictionary

        Parameters:
        data: dict: [str,int] dict with key,values symbol and their
        corresponding frequency in the text as value.

        Returns
        ------
        list
        '''
        node_list = []
        for key, value in sorted(char_freq.items(), key=lambda val: val[1]):
            node_list.append(node.Node(key, value))
        heapify(node_list)
        return node_list

    @classmethod
    def build_huffman_tree(cls, heap_list: list) -> list:
        '''
        Traverses the whole tree to buid the corresponding tree with help
        from the Node class.
        '''
        while len(heap_list) > 1:
            lnode = heapq.heappop(heap_list)
            rnode = heapq.heappop(heap_list)
            pnode = node.Node(None, lnode.get_freq() + rnode.get_freq())
            pnode.set_childs(lnode, rnode)
            heapq.heappush(heap_list, pnode)
        return heapq.heappop(heap_list)

    def build_tree_dict(self, node: node.Node, code: int) -> dict:
        '''
        Builds the huffman tree recursively.
        '''
        if node is None:
            return
        if self._print_tree:
            print(f'Symbol: {node.get_symbol()},\
                    Freq: {node.get_freq()},\
                    Code: {code},\
                    Leaf node: {node.get_symbol() is not None}')
        if node.get_symbol() is not None:
            self._tree[node] = bitarray(code)

        self.build_tree_dict(node.get_lchild(), code + '0')
        self.build_tree_dict(node.get_rchild(), code + '1')
