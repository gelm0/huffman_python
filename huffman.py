#!/usr/bin/python3
import heapq
import sys
from heapq import heapify
from heapq import heappop

codes_dict = {}

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

def count_freq(txt):
    freq = {}
    for c in txt:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq

def make_codesdict(node, code):
    if node == None:
        return
    
    if node._symbol != None:
        codes_dict[node._symbol] = code
        return

    make_codesdict(node._left_child, code + "0")
    make_codesdict(node._right_child, code + "1")

def compress(txt):
    return "".join([codes_dict[c] for c in txt])

f = open('testfile', 'rb').read()
freq = count_freq(f)
node_list = []
for k,v in sorted(freq.items(), key=lambda val : val[1]):
    node_list.append(Node(k,v))
heapify(node_list)

#for i in node_list:
#    print(i._symbol, i._freq)
# Debug purposes
#for node in node_list:
#    print(node.get_freq())

while len(node_list) > 1:
    lnode = heapq.heappop(node_list)
    rnode = heapq.heappop(node_list)
    pnode = Node(None, lnode._freq + rnode._freq)
    pnode.set_childs(lnode, rnode)
    heapq.heappush(node_list, pnode) 

# Pop the last item, the root node and traverse
root = heapq.heappop(node_list)
make_codesdict(root, "")
comp = compress(f)
fcomp = open('compfile', 'wb')
fcomp.write(str.encode(comp))
print(sys.getsizeof(f), sys.getsizeof(comp))
#print(node_list[0].get_freq())
