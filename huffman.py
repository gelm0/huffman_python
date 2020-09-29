#!/usr/bin/python3
import heapq
import sys
from bitarray import bitarray
from heapq import heapify,heappop

class Node:
    def __init__(self, symbol, freq):
        self._symbol = symbol;
        self._freq = freq
        self._left_child = None
        self._right_child = None

    def __lt__(self, other):
        return self._freq < other._freq

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if other == None:
            return False
        return self._freq == other._freq

    def set_childs(self, lchild, rchild):
        self._right_child = rchild
        self._left_child = lchild

    def get_rchild(self):
        return self._right_child

    def get_lchild(self):
        return self._right_child

class Huffman:
    def __init__(self):
        self.codes_dict = {}        
        self.bitarray_dict = {}

    def count_freq(self, txt):
        freq = {}
        for c in txt:
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1
        return freq

    def make_codes_dict(self, node, code):
        if node == None:
            return
    
        if node._symbol != None:
            self.codes_dict[node._symbol] = code
            return

        self.make_codesdict(node._left_child, code + "0")
        self.make_codesdict(node._right_child, code + "1")

    def make_bitarray_codes_dict(self):
        

    def encode_file(self, file_name):
        file_data = open(file_name, 'rb').read()
        self.encode(file_data)

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

    def encode(self, file_data):
        char_freq = self.count_freq(file_data)
        heap_list = self.heapify_tree(char_freq) 
        root = self.build_huffman_tree(heap_list)
        self.make_codes_dict(root, "")
        print(self.codes_dict)

    def test_compress(self, txt):
        encode = bitarray()
        print(encode.encode(self.codes_dict, txt))


    def compress(self, txt):
        return "".join([self.codes_dict[c] for c in txt])

# https://pypi.org/project/bitarray/
# We need to construct a bitarray encoding dict.
f = open('testfile', 'rb').read()
huffman = Huffman()
huffman.encode_file('testfile')
output = huffman.compress(f)
output_file = open('output_binary', 'wb')
print(output)
print(output.encode())
huffman.test_compress(f)

output_file.write(output.encode())
#huffman = Huffman()
#freq = huffman.count_freq(f)
#node_list = []
#for k,v in sorted(freq.items(), key=lambda val : val[1]):
#    node_list.append(Node(k,v))
#heapify(node_list)

# Pop the last item, the root node and traverse
#root = heapq.heappop(node_list)
#make_codesdict(root, "")
#comp = compress(f)
#fcomp = open('compfile', 'wb')
#fcomp.write(str.encode(comp))
#print(sys.getsizeof(f), sys.getsizeof(comp))
#print(node_list[0].get_freq())

#for i in node_list:
#    print(i._symbol, i._freq)
# Debug purposes
#for node in node_list:
#    print(node.get_freq())

