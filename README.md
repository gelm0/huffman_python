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

python3 huffman.py <OPTIONS>

- -h or --help



#### API

#### Further implementation
In the future I would like to implement the LZ78 algorithm together with this library as well. Shouldn't be a huge task but currently looking at some other sideprojects so I am going to have comeback to this.
