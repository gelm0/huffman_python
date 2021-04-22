import argparse
import os.path
import bitarray
import huffmantree
from bitarray import decodetree

__VERBOSE__ = False


class HuffmanInitException(Exception):
    '''
    Exception to be thrown when Huffman tree has not been initialized
    '''
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return f'Huffman tree has not been initialized properly.\
                {self._message}.'


class HuffmanHeaderException(Exception):
    '''
    To be thrown header is missing or we are unable to read the it correcly
    '''
    def __str__(self):
        return 'Header missing or could not be decoded properly.'


def compress_file(input_file, output_file):
    '''Attempts to open and read from the supplied input_file.
    If successful will construct a huffman tree from the data contained in\
    the text and huffman encode the data contained in the input_file and\
    write it to the output_file.

    TODO: Input needs to be larger then one char. Input > 1

    Parameters
    ---------
    input_file: file, required
        The file which content should be compressed.

    output_file: file, required
        The output file which where the encoded data should be written.
    '''
    huffman = huffmantree.HuffmanTree(print_tree=__VERBOSE__)
    symbol_tree = huffman.get_symbol_tree(file_name=input_file)
    with open(input_file, 'r') as fin, open(output_file, 'wb') as fout:
        compressed_data = compress(symbol_tree, fin.read())
        fout.write(compressed_data)


def decompress_file(input_file, output_file):
    '''Attempts to open and read from the supplied input_file.
    If successful will try and construct a huffman tree from the header\
            contents in the
    input_file. The huffman tree will then be used to try and decode the data.
    If successful will write the decoded data to the supplied output file.

    Parameters
    ---------
    input_file: file, required
        The file which content should be decompressed.

    output_file: file, required
        The output file which where the decoded data should be written.

    Raises
    -----
    HuffmanHeaderException
        If header can't be decoded or the file doesn't contain a valid header.
    '''
    with open(input_file, 'r') as fin, open(output_file, 'wb') as fout:
        decompressed_data = decompress(fin.read())
        fout.write(decompressed_data)


def compress(symbol_tree, data):
    '''
    Main function for compressing
    '''
    header = construct_header(symbol_tree)
    encoded_data = encode(symbol_tree, data)

    return header + encoded_data


def decompress(compressed_data):
    '''
    Main function for decompressing
    '''
    header, encoded_data = deconstruct_compressed_data(compressed_data)
    symbol_tree = read_header(header)

    return decode(symbol_tree, encoded_data)


def construct_header(symbol_tree: dict):
    '''Builds the header from left to right based on the tree 

    Parameters
    ---------
    symbol_tree: dict
        Contains the dict over the respective symbols and their huffman codes

    Returns
    ------
        A binary string with the following format
        All left nodes start with a 0 so we can safely remove the first bit.
        Thus all codes in the left tree will have len(code) - 1
        Respectively all nodes in the right part of the tree starts with a 1.
        Thus the output will be something like this:
        b'00,a\n001,s\n-1\n01s\nn101\n'
        The negative integer represents switch from left to right.
    '''
    symbols = b''
    left_tree_visited = False

    for symbol, code in symbol_tree.items():
        if not left_tree_visited and code.to01().startswith('1'):
            symbols += b'-1\n'
            left_tree_visited = True
        symbols += b'%d,%s\n' % (ord(symbol), code.to01()[1:].encode())

    return symbols[:-1] + b'\n'


def encode(symbol_tree: dict, text: str):
    '''Compresses a string based text to bytes based on a huffman tree'''
    encode = bitarray()
    encode.encode(symbol_tree, text)
    unused = encode.buffer_info()[3]
    unused_buffer = b'%d\n' % unused

    return unused_buffer + encode.tobytes()

def deconstruct_compressed_data(compressed_data):
    split_data = compressed_data.split(b'\n')
    header = split_data[0]
    unused = int(split_data[1])
    encoded_data = b'\n'.join(split_data[2:])

    if unused > 0:
        del encoded_data[-unused:]

    return header, encoded_data


def read_header(header: bin):
    '''Constructs a huffman dictionary from the header {symbol, bitarray}'''
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


def decode(symbol_tree: dict, encoded_data: bin):
    '''Decompresses bytes in data into it's original format'''
    encoded = bitarray()
    encoded.frombytes(encoded_data)
    decode_tree = decodetree(symbol_tree)
    return encoded.decode(decode_tree)


def check_input(input_file: str, output_file: str):
    if not input_file:
        print('No input file is supplied')
        exit(-1)

    if not output_file:
        print('No output file is supplied')
        exit(-1)
    
    if not os.path.isfile(input_file):
        print('Input file doesn\'t exist')
        exit(-1)

    if os.path.isdir(output_file):
        print('Output file can\'t be a directory')
        exit(-1)

    if (dir_split := output_file.rfind('/')) > 0:
        if not os.path.exists(output_file[:dir_split + 1]):
            print('Specified path to output file doesn\'t exist')
            exit(-1)


def main():
    '''
    Main interactive function
    '''
    parser = argparse.ArgumentParser(
            description='Huffman encode and decode files.')
    parser.add_argument('--compress', '-c', action='store_true',
                        help='Compress a file')
    parser.add_argument('--decompress', '-d', action='store_true',
                        help='Decompress a file')
    parser.add_argument('--input', '-i', action='store',
                        help='Path to the input file\
                                where content should be read from')
    parser.add_argument('--output', '-o', action='store',
                        help='Path to the output file where\
                                content should be written')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    args = parser.parse_args()
    if args.compress and args.decompress:
        print('\nCan\'t compress and decompress files at the same time\n')
        parser.print_help() 
        exit(-1)

    # Check that all input is valid and exists
    check_input(args.input, args.output)

    __VERBOSE__ = args.verbose

    if args.compress:
        if __VERBOSE__:
            print(f'Compressing {args.input} and writing data to {args.output}')
        compress_file(args.input, args.output)

    if args.decompress:
        pass


if __name__ == '__main__':
    main()
