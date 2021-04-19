import heapq
import sys
from node import Node
from bitarray import bitarray, decodetree
from heapq import heapify,heappop

class Huffman:
    def get_symbol_tree(tree):
        return dict(sorted(dict(map(lambda node: (node[0]._symbol, node[1]), tree.items())).items(), key = lambda val : val[1]))

    def build_tree_from_file(self, file_name):
        file_data = open(file_name, 'r').read()
        return self.build_tree(file_data)

    def build_tree(self, data):
        char_freq = self.count_freq(data)
        heap_list = self.heapify_tree(char_freq) 
        root = self.build_huffman_tree(heap_list)
        code_dict = {}
        self.make_codes_dict(code_dict, root, '')
        return code_dict

    def count_freq(self, data):
        freq = {}
        for c in data:
            freq[c] = freq[c] + 1 if c in freq else 1
        return freq

    def heapify_tree(self, char_freq):
        node_list = []
        for k,v in sorted(char_freq.items(), key=lambda val : val[1]):
            node_list.append(Node(k,v))
        heapify(node_list)
        return node_list

    def build_huffman_tree(self, heap_list):
        while len(heap_list) > 1:
            lnode = heapq.heappop(heap_list)
            rnode = heapq.heappop(heap_list)
            pnode = Node(None, lnode._freq + rnode._freq)
            pnode.set_childs(lnode, rnode)
            heapq.heappush(heap_list, pnode) 
        return heapq.heappop(heap_list)

    def make_codes_dict(self, code_dict, node, code, print_tree=False):
        if node == None:
            return
        if print_tree:
            print(f'Symbol: {node._symbol},\
                    Freq: {node._freq},\
                    Code: {code},\
                    Leaf node: {node._symbol != None}')
        if node._symbol != None:
            code_dict[node] = bitarray(code)

        self.make_codes_dict(code_dict, node.get_lchild(), code + '0', print_tree)
        self.make_codes_dict(code_dict, node.get_rchild(), code + '1', print_tree)

    '''Compresses a string based text to bytes based on a huffman tree'''
    @staticmethod
    def compress(code_dict, text):
        encode = bitarray()
        encode.encode(code_dict, text)
        unused = encode.buffer_info()[3]
        unused_buffer = b'%d\n' % unused
        return unused_buffer + encode.tobytes()

    '''Decompresses bytes in data into it's original format'''
    @staticmethod
    def decompress(code_dict, data):
            encoded = bitarray()
            split_data = data.split(b'\n')
            unused = int(split_data[0])
            compressed = b'\n'.join(split_data[1:])
            encoded.frombytes(compressed)
            # Remove unused filling
            if unused > 0:
                del encoded[-unused:]
            decode_tree = decodetree(code_dict)
            return encoded.decode(decode_tree)

    '''Builds the huffman tree from left to right'''
    @staticmethod
    def write_header(symbol_tree):
        symbols = b''
        left_tree_visited = False
        for k,v in symbol_tree.items():
            if not left_tree_visited and v.to01().startswith('1'): 
                symbols += b'-1\n'
                left_tree_visited = True
            symbols += b'%d,%s\n' % (ord(k), v.to01()[1:].encode())
        return symbols[:-1]
    
    '''Constructs a huffman dictionary from the header {symbol, bitarray}'''
    @staticmethod
    def read_header(header):
        symbol_tree = {}
        # We start from the left
        tree_path_prefix = '0'
        left_tree_visited = False
        for s in header.split():
            if not left_tree_visited and s == b'-1':
                tree_path_prefix = '1'
                left_tree_visited = True
                continue
            val = s.decode().split(',')
            symbol_tree[chr(int(val[0]))] = bitarray(tree_path_prefix + val[1])
        return symbol_tree

if __name__ == '__main__':
    # Returns left sorted huffman tree dict {symbol, bitarray}


''' Docs '''
''' Line 1 is always header content, Line 2 always contains content, Line 3 is optional and will be written out if unused bytes is contained in the content ''' 
''' TODO: Input needs to be larger then one char. Input > 1'''
