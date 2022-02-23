import os
from math import ceil
from collections import Counter
from knuth import encode_gray_knuth, decode_gray_knuth, find_decoded_length2

from sympy.combinatorics.graycode import GrayCode
import pytest


def main():
    gray_codes = GrayCode(10)
    print(list(gray_codes.generate_gray()))


@pytest.mark.parametrize('k', [4, 7, 10, 13])
def test_gray_knuth(k):
    c = Counter()
    for i in range(2 ** k):
        original = bin(i)[2:].zfill(k)
        encoded = encode_gray_knuth(original)
        assert (encoded is not None)
        count_bits = Counter(encoded)
        assert (abs(count_bits['0'] - count_bits['1']) <= 1)
        c.update([encoded])
        decoded = decode_gray_knuth(encoded)
        assert(decoded == original)
    assert (max(c.values()) == 1)


@pytest.mark.parametrize('length', [150, 200, 500, 1000])
def test_random_long_data(length):
    for _ in range(100):
        random_bytes = os.urandom(ceil(length / 8))
        original = ''.join([bin(byte)[2:] for byte in random_bytes])[:length]
        encoded = encode_gray_knuth(original)
        assert (encoded is not None)
        count_bits = Counter(encoded)
        assert (abs(count_bits['0'] - count_bits['1']) <= 1)
        decoded = decode_gray_knuth(encoded)
        assert (decoded == original)


@pytest.mark.parametrize("encoded_length, decoded_length", [
    (11, 7),
    (13, 8)
])
def test_find_decoded_length(encoded_length, decoded_length):
    assert(find_decoded_length2(encoded_length) == decoded_length)
