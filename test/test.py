import os
import sys
import filecmp
import unittest
from compression import huffmantree, huffman


def test_compress(file_name):
    with open(file_name, 'rb') as fin:
        data_read = fin.read()
        compressed_data = huffman.encode_data(data_read)
        decompressed_data = huffman.decode_data(compressed_data)
        return data_read, decompressed_data

def test_compress_canon(file_name):
    with open(file_name, 'rb') as fin:
        data_read = fin.read()
        compressed_data = huffman.encode_data(data_read, True)
        decompressed_data = huffman.decode_data(compressed_data)
        return data_read, decompressed_data

def get_symbol_tree(data):
    h = huffmantree.HuffmanTree(data=data)
    h.get_symbol_tree_by_val()


class HuffmanTest(unittest.TestCase):

    resources = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
                                + '/test/resources/'
    test_file_1 = resources + 'short_text.txt'
    test_file_2 = resources + 'medium_text.txt'
    test_file_3 = resources + '84-h.htm'

    def test_shorter_string_huffman(self):
        data_read, decompressed_data = test_compress(self.test_file_1)
        assert data_read == decompressed_data

    def test_shorter_string_canon(self):
        data_read, decompressed_data = test_compress_canon(self.test_file_1)
        assert data_read == decompressed_data

    def test_longer_string_huffman(self):
        data_read, decompressed_data = test_compress(self.test_file_2)
        assert data_read == decompressed_data

    def test_longer_string_canon(self):
        data_read, decompressed_data = test_compress_canon(self.test_file_2)
        assert data_read == decompressed_data

    def test_frankenstein_book_huffman(self):
        data_read, decompressed_data = test_compress(self.test_file_3)
        assert data_read == decompressed_data

    def test_frankenstein_book_canon(self):
        data_read, decompressed_data = test_compress_canon(self.test_file_3)
        assert data_read == decompressed_data

    def test_encode_decode_canon_header(self):
        h = huffmantree.HuffmanTree(file_name=self.test_file_1)
        symbol_tree = h.get_canon_tree()
        header = huffman.construct_canonical_header(symbol_tree)
        deserialized_header, _ = huffman.deconstruct_encoded_data(header
                                                                  + b'0\n0')
        expected_symbol_tree =\
            huffman.read_canonical_header(deserialized_header)
        assert symbol_tree == expected_symbol_tree

    def test_encode_decode_header(self):
        h = huffmantree.HuffmanTree(file_name=self.test_file_1)
        symbol_tree = h.get_symbol_tree_by_val()
        header = huffman.construct_header(symbol_tree)
        deserialized_header, _ = huffman.deconstruct_encoded_data(header
                                                                  + b'0\n0')
        expected_symbol_tree = huffman.read_header(deserialized_header)
        assert symbol_tree == expected_symbol_tree

    def test_full_program_flow(self):
        outfile = 'out'
        outfile_decomp = 'outd'
        outfile_canon = 'outc'
        outfile_canon_decomp = 'outdc'
        sys.argv = ['', '-i', self.test_file_3, '-o', outfile, '-e']
        huffman.main()
        sys.argv = ['', '-i', self.test_file_3, '-o',
                    outfile_canon, '-e', '-c']
        huffman.main()
        sys.argv = ['', '-o', outfile_decomp, '-i', outfile, '-d']
        huffman.main()
        sys.argv = ['', '-o', outfile_canon_decomp,
                    '-i', outfile_canon, '-d']
        huffman.main()

        assert(filecmp.cmp(self.test_file_3, outfile_decomp, shallow=False))
        assert(filecmp.cmp(self.test_file_3, outfile_canon_decomp, shallow=False))
        


if __name__ == '__main__':
    unittest.main()
