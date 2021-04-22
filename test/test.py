if __name__ == '__main__':
    main()

def main(*args, **kwargs):
    def test_compress_decompress(data, description):
        print(f'Trying to compress and decompress {description}')
        huffman = Huffman()
        # Build tree
        tree = huffman.build_tree(data)
        # Get huffman symbol tree needed for bitarray
        symbol_tree = get_symbol_tree(tree)
        # Create header based on the symbol tree
        header = huffman.write_header(symbol_tree)
        # Huffman compression based on the symbol tree (Non canonical)
        compressed_data = huffman.compress(symbol_tree, data)
        # Reconstruct symbol tree from previously created header
        read_symbol_tree = huffman.read_header(header)
        # Decompression of the data using the reconstructed header
        decompressed_data = huffman.decompress(read_symbol_tree, compressed_data)
        # Decompressed data
        restored_data = ''.join(str(c) for c in decompressed_data)
    
        assert read_symbol_tree == symbol_tree, 'Huffman tree read from header is equivalent to constructed huffman tree from data'
        assert data == restored_data, 'Initial data equivalent to restored data'
    
    
    test_string_1 = "These boots are made for walking but these trees are not."
    test_string_2 = "st" test_string_3 = "sti"
    test_string_4 = 'a'
    test_string_6 = ' '
    test_string_7 = ''
    test_string_7 = '''Jane Austen (/ˈɒstɪn, ˈɔːs-/; 16 December 1775 – 18 July 1817) was an English novelist known primarily for her six major novels, which interpret, critique and comment upon the British landed gentry at the end of the 18th century. Austen's plots often explore the dependence of women on marriage in the pursuit of favourable social standing and economic security. Her works critique the novels of sensibility of the second half of the 18th century and are part of the transition to 19th-century literary realism.[2][b] Her use of biting irony, along with her realism, humour, and social commentary, have long earned her acclaim among critics, scholars, and popular audiences alike.[4]

    With the publication of Sense and Sensibility (1811), Pride and Prejudice (1813), Mansfield Park (1814) and Emma (1816), she achieved success as a published writer. She wrote two other novels, Northanger Abbey and Persuasion, both published posthumously in 1818, and began another, eventually titled Sanditon, but died before its completion. She also left behind three volumes of juvenile writings in manuscript, the short epistolary novel Lady Susan, and another unfinished novel, The Watsons. Her six full-length novels have rarely been out of print, although they were published anonymously and brought her moderate success and little fame during her lifetime.
    
    A significant transition in her posthumous reputation occurred in 1833, when her novels were republished in Richard Bentley's Standard Novels series, illustrated by Ferdinand Pickering, and sold as a set.[5] They gradually gained wider acclaim and popular readership. In 1869, fifty-two years after her death, her nephew's publication of A Memoir of Jane Austen introduced a compelling version of her writing career and supposedly uneventful life to an eager audience.
    
    Austen has inspired many critical essays and literary anthologies. Her novels have inspired many films, from 1940's Pride and Prejudice to more recent productions like Sense and Sensibility (1995), Emma (1996), Mansfield Park (1999), Pride & Prejudice (2005), Love & Friendship (2016), and Emma (2020).[c]'''
    
    
    test_compress_decompress(test_string_1, 'easy string')
    test_compress_decompress(test_string_2, 'string of length 2')
    test_compress_decompress(test_string_3, 'string of length 3')
    #test_compress_decompress(test_string_4)
    #test_compress_decompress(test_string_5)
    #test_compress_decompress(test_string_6)
    #test_compress_decompress(test_string_7)
