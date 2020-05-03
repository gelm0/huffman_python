#!/usr/bin/python3

class node:
    def __init__(self, symbol, freq):
        self._symbol = symbol;
        self._freq = freq
        self._left_child = None
        self._right_child = None

    def set_right_child(self, child):
        self._right_child =  child

    def set_left_child(self, child):
        self._left_child = child

    def get_right_child(self):
        return self._right_child

    def get_left_child(self):
        return self._right_child

    def get_freq(self):
        return self._freq 

def count_freq(txt):
    freq = {}
    for c in txt:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq

f = open('testfile', 'rb').read()
freq = count_freq(f)
node_list = []
for k,v in sorted(freq.items(), key=lambda val : val[1]):
    node_list.append(node(k,v))
    print(k,v)
