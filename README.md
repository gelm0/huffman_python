### Huffman encoder/decoder
A Python implementation of huffman encoding and decoding text files using the [bitarray](https://pypi.org/project/bitarray/) library. Yes I am aware that the library already has some functionality that supports this but I wrote this simply for the intent of learning more about compression.

The implementation also has a command line utility which you can use to encode and decode files using both standard and canonical huffman encoding.

#### Installation and tests
For easier separation of environments I would reccomend to install virtualenvwrapper, which allows you to create a separate environment. Great for development when you want to keep track of dependencies and versions. Installation instructions can be found [here](https://virtualenvwrapper.readthedocs.io/en/latest/)

The code was developed on **Python 3.9**

```sh
# Optional
mkvirtualenv huffman
workon huffman

# Installation
git clone https://github.com/gelm0/huffman_python.git
cd huffman_python
python3 setup.py install

# Run tests
python3 setup.py test
```

#### CLI Usage

python3 huffman.py *OPTIONS*

- **-h or --help** Shows available options
- **-e or --encode** Encode a file (This or decode option must be supplied)
- **-d or --decode** Decode a file (This or encode option must be supplied)
- **-i or --input** Input file. Raw text format if file is to be decoded or encoded file if to be decoded.
- **-o or --output** Output file of the decoded/encoded file.
- **-c or --canon** If the file is to be encoded with canonical format.
- **-v or --verbose** Shows some extra verbose output while constructing the huffman tree. 
#### API
If anyone wishes to try the code out the main encoding/decoding algorithms recides in compression/huffmantree.py while the header encoding mechanisms recides in huffman.py

```python
from compression import huffman

#Encode file non canonical
# Just supply filenames of the input and output file
huffman.encode_file('example_file', example_output')

#Decode file
huffman.encode_file('example_output', example_file_decoded')

#Encode bytes
example_string = b'this is a test string'
encoded_data = huffman.encode_data(example_string)

#Decode bytes
decoded_data = huffman.decode_data(encoded_data)
```

#### Further implementation
In the future I would like to implement the LZ78 algorithm together with this library as well. Shouldn't be a huge task but currently looking at some other sideprojects so I am going to have comeback to this.
