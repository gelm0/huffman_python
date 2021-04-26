'''
Huffman compress/decompress
'''
import argparse
import sys
import os.path
from bitarray import bitarray, decodetree
import huffmantree

__verbose__ = False


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
    huffman = huffmantree.HuffmanTree(print_tree=__verbose__)
    symbol_tree = huffman.get_symbol_tree(file_name=input_file)
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
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
    '''
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        decompressed_data = decompress(fin.read())
        fout.write(decompressed_data)


def compress(symbol_tree: dict, data: bytes) -> bytes:
    '''
    Main function for compressing

    Construct header from huffman tree then encodes data and returns result
    
    The header contains a line for each symbol with corresponding huffman code
    which is followed by the binary data. The last line in the binary content
    is reserved for how much padding we need to remove when decompressing the 
    content again.
    '''
    header = construct_header(symbol_tree)
    encoded_data = encode(symbol_tree, data)
    return header + encoded_data


def decompress(compressed_data: bytes) -> bytes:
    '''
    Main function for decompressing

    '''
    header, encoded_data = deconstruct_compressed_data(compressed_data)
    symbol_tree = read_header(header)
    return decode(symbol_tree, encoded_data)


def construct_header(symbol_tree: dict) -> bytes:
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
            symbols += b'-1, -1\n'
            left_tree_visited = True
        symbols += b'%x,%s\n' % (symbol, code.to01()[1:].encode())

    # Need an indicator to know where header ends
    return symbols + b'HEND\n'


def encode(symbol_tree: dict, text: bytes) -> bytes:
    '''
    Compresses binary content to bytes based on a huffman tree contained in
    symbol tree.

    Parameters
    ---------
    symbol_tree:
        dict with key,values of symbol_tree[symbol] = bitarray(huffman_code)
    text:
        binary content to be encoded

    Returns
    -------
    bytes:
        encoded data followed by newline and unused bytes i.e.
        how much padding we need to remove when decoding
    '''
    encode = bitarray()
    encode.encode(symbol_tree, text)
    unused = encode.buffer_info()[3]
    unused_buffer = b'%d' % unused

    return encode.tobytes() + b'\n' + unused_buffer

def deconstruct_compressed_data(compressed_data: bytes) -> (dict, bitarray):
    '''
    Splits the encoded data into their respective parts
    
    Extracts three parts from the encoded data: huffman tree, data, padding
    Will return a huffman tree and the data with the removed padding.

    Parameters
    ---------
    compressed_data:
        Binary huffman encoded content

    Returns 
    -------
        header: dict
            The decoded header in a dict containing the decoded huffman symbol
            tree
        encoded_data: bitarray:
            The actual encoded data as a bitarray
    '''
    split_data = compressed_data.split(b'\n')
    header = {}
    data_start = -1
    for index, line in enumerate(split_data):
        if line == b'HEND':
            data_start = index + 1
            break
        keyval = line.decode().split(',')
        header[keyval[0]] = keyval[1]
    unused = int(split_data[-1], 16)
    encoded_data = split_data[data_start:-1]
    bitdata = bitarray()
    bitdata.frombytes(b'\n'.join(encoded_data))

    if unused > 0:
        del bitdata[-unused:]

    return header, bitdata


def read_header(header: dict) -> dict:
    '''Constructs a huffman dictionary from the header {symbol, bitarray}'''
    symbol_tree = {}
    # We start from the left
    tree_path_prefix = '0'
    left_tree_visited = False

    for key, val in header.items():
        if not left_tree_visited and key == '-1':
            tree_path_prefix = '1'
            left_tree_visited = True
            continue

        symbol_tree[int(key, 16)] = bitarray(tree_path_prefix + val)

    return symbol_tree


def decode(symbol_tree: dict, encoded_data: bytes) -> bytes:
    '''Decompresses bytes in data into it's original format'''
    decode_tree = decodetree(symbol_tree)
    return bytearray(encoded_data.decode(decode_tree))




def check_input(input_file: str, output_file: str) -> None:
    '''
    Checks input and output file of user input in main function
    Exits with a negative value if it finds any errors otherwise
    does nothing
    '''
    if not input_file:
        exit_with_message('No input file is supplied')

    if not output_file:
        exit_with_message('No output file is supplied')
 
    if not os.path.isfile(input_file):
        exit_with_message('Input file doesn\'t exist')

    if os.path.isdir(output_file):
        exit_with_message('Output file can\'t be a directory')

    if (dir_split := output_file.rfind('/')) > 0:
        if not os.path.exists(output_file[:dir_split + 1]):
            exit_with_message('Specified path to output file doesn\'t exist')


def exit_with_message(message: str, exitcode: int = -1) -> None:
    """
    Print message to stdout before exit
    """
    print(message)
    sys.exit(exitcode)


def main() -> None:
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
        sys.exit(-1)

    # Check that all input is valid and exists
    check_input(args.input, args.output)

    __verbose__ = args.verbose

    if args.compress:
        if __verbose__:
            print(f'Compressing {args.input} and writing data to\
                    {args.output}')
        compress_file(args.input, args.output)

    if args.decompress:
        decompress_file(args.input, args.output)


if __name__ == '__main__':
    main()
