# BalancedCodesKnuth

This project is an improved implementation of Knuth's algorithm for balanced codes, given in "Efficient Balanced Codes", IEEE Transactions on Information Theory, vol. 32,
no. 1, pp. 51–53, Jan. 1986. 

This implementation uses gray-code in order to reduce the require reduandency bits or the recursevly iteration of the aglorithm.

A documented details can be seen in *description.pdf* file.

## Getting Started

### Prerequisites
This project requires Python 3 for running it.
In addition, it uses SymPy library and require its installation. 


## tests
Our tests check various words, and make sure all the code is filling all the require conditons.

We have a "check_encoding" function that gets a word to encdoe, encode it, and checks:
1. is the algorithm was able to encode this word
2. is the encoded word is balanced
3. is the decoded word is equal to to original word

we used this "check_encoding" tested our algorithm on various word codes,
in different lenghts.

Initally we test our algorithm on all the vectors under 13 bits.
After passing all the tests for those words, we added tests for long information vectors.

We choose randomly 100 vectors in different (and big) lenghts (for example, 500 or 1000),
and we test sucssesfully our encoding algorithm on those vectors.


## Authors

* **Yuval Goldberg**
* **Itay Nakash**
