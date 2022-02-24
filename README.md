# GrayCodeKnuth

This project is an improved implementation of Knuth's algorithm for balanced codes, given in "Efficient Balanced Codes", IEEE Transactions on Information Theory, vol. 32,
no. 1, pp. 51–53, Jan. 1986.

This implementation uses Gray-code in order to reduce the required redundancy bits or the recursive iteration of the algorithm.

This implementation is based on the binary version of the algorithm given in "A construction for balancing non-binary sequences based on gray code prefixes", E. N. Mambou and T. G. Swart, IEEE Transactions on Information Theory.

Documented details can be seen in *description.pdf* file.

## Getting Started

### Prerequisites
This project requires Python 3 for running it.
In addition, it uses SymPy library and require its installation. 

### Installation

In order to install all the relevant libraries for running and testing, run (in the root dir of the project):
```shell
python3 setup.py install
```

### Importing

Add the following lines:
```python
from gray_knuth import encode_gray_knuth, decode_gray_knuth
encoded_data = encode_gray_knuth('100101100')
decoded_data = decode_gray_knuth(encoded_data)
decode_gray_knuth(encoded_data, decoded_length=9)
```

## Tests
Our tests check various words, and make sure all the code is filling all the required conditions.

We have a `check_encoding` function that gets a word to encode, encodes it, and checks:
1. That the algorithm was able to encode this word.
2. That the encoded word is properly balanced.
3. That decoding the encoded word results in the same word as the original word.

We used this `check_encoding` to test our algorithm on various words of different lengths.

Initially we test our algorithm on all the vectors under 13 bits.
After passing all the tests for those words, we added tests for long information vectors.
We choose randomly 100 vectors in different (and long) lengths (for example, 500 or 1000),
and we test our encoding algorithm on those vectors.

### Run tests

After installing the package, run:
```shell
pytest
```

## Authors

* **Yuval Goldberg**
* **Itay Nakash**
