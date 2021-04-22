"""
Huffmantree implementation
"""
import heapq
from heapq import heapify
import bitarray
from node import Node


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

    Attributes
    ---------
    print_tree: boolean, optional, default False
        Prints the whole huffman tree when it's being constructed with
        symbol, frequency, huffman code and if it's a leaf node
    endian: str, optional, default 'big'
        endianess of bitarray used.
    '''
    def __init__(self, endian='big', print_tree=False):
        self._print_tree: bool = print_tree
        self._endian: str = endian
        self._tree: dict = {}

    # Might need a deep copy here if this fucks with the original node tree
    def get_symbol_tree(self, file_name: str = None, data: str = None):
        '''
        Creates a huffman tree dict. ['symbol': bitarray(Huffman Code)]

        Parameters
        ---------
        file_name: str, optional
            Name of the file which content should be used to construct the huffman tree.
        data: str, optional
            Input string which should be used to construct the huffman tree.
        If both are supplied the file_name will take precident.

        Returns
        ------
        A dictionary of key,values with types [str, bitarray] where the bitarray contains the
        corresponding huffman code for the symbol.

        Raises
        -----
        HuffmanInitException if neither file_name or data is supplied
        '''
        self.check_tree_init(file_name, data)
        return dict(sorted(dict(map(lambda node: (node[0].get_symbol(), node[1]),\
                self._tree.items())).items(),\
                key = lambda val : val[1]))

    def get_tree(self, file_name: str = None, data: str = None):
        '''
        Creates a huffman tree dict. ['Node': bitarray(Huffman Code)]

        Parameters
        ---------
        file_name: str, optional
            Name of the file which content should be used to construct the huffman tree.
        data: str, optional
            Input string which should be used to construct the huffman tree.
        If both are supplied the file_name will take precident.

        Returns
        ------
        A dictionary of key,values with types [Node, bitarray] where the bitarray contains the
        corresponding huffman code for the Node.

        Raises
        -----
        HuffmanInitException if neither file_name or data is supplied
        '''
        self.check_tree_init(file_name, data)
        return self._tree

    def check_tree_init(self, file_name: str, data: str):
        '''
        Initializes the huffman tree
        '''
        self.tree_init(file_name, data)
        if not self._tree:
            raise HuffmanInitException('Please supply data or file_name to '\
                    'initialize the huffman tree')

    def tree_init(self, file_name: str, data: str):
        '''
        Tries to initialize the huffman tree with from the file_name. If that isin't supplied
        tries with data instead.
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
        with open(file_name, 'r') as fin:
            self.build_tree_from_data(fin.read())

    def build_tree_from_data(self, data: str):
        '''
        Responsible for the build flow of the huffman tree.
        First creates a dictionary of all corresponding characters frequency in the supplied data.
        Then constructs a minheap with the lowest frequency node as root
        Lastly the tree is traversed bottom-up to construct the huffman tree.

        Parameters
        ---------
        data: str, the supplied content for which the huffman tree is created.
        '''
        char_freq = self.count_freq(data)
        heap_list = self.heapify_freq(char_freq)
        root = self.build_huffman_tree(heap_list)
        self.build_tree_dict(root, '')

    @classmethod
    def count_freq(cls, data: str):
        '''
        Counts the frequency of all characters in supplied string.

        Parameters:
        data: str, the supplied content for which the frequency should be calculated.

        Returns
        ------
        dict with [char: str, frequency: int]
        '''
        freq = {}
        for char in data:
            freq[char] = freq[char] + 1 if char in freq else 1
        return freq

    @classmethod
    def heapify_freq(cls, char_freq: dict):
        '''
        Constructs a min heap from a dictionary

        Parameters:
        data: dict: [str,int] dict with key,values symbol and their corresponding frequency in the
        text as value.

        Returns
        ------
        list
        '''
        node_list = []
        for key,value in sorted(char_freq.items(), key=lambda val : val[1]):
            node_list.append(Node(key,value))
        heapify(node_list)
        return node_list

    @classmethod
    def build_huffman_tree(cls, heap_list: list):
        '''
        Traverses the whole tree to buid the corresponding tree with help from the Node class.
        '''
        while len(heap_list) > 1:
            lnode = heapq.heappop(heap_list)
            rnode = heapq.heappop(heap_list)
            pnode = Node(None, lnode.get_freq() + rnode.get_freq())
            pnode.set_childs(lnode, rnode)
            heapq.heappush(heap_list, pnode)
        return heapq.heappop(heap_list)

    def build_tree_dict(self, node: Node, code: int):
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
            self._tree[node] = bitarray(code, endian=self._endian)

        self.build_tree_dict(node.get_lchild(), code + '0')
        self.build_tree_dict(node.get_rchild(), code + '1')
