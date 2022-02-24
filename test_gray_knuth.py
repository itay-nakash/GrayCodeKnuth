import os
from collections import Counter
from math import ceil

import pytest

from gray_knuth import encode_gray_knuth, decode_gray_knuth, find_decoded_length


def check_encoding(original):
    encoded = encode_gray_knuth(original)
    assert (encoded is not None)
    count_bits = Counter(encoded)
    assert (abs(count_bits['0'] - count_bits['1']) <= 1)
    decoded = decode_gray_knuth(encoded)
    assert (decoded == original)
    return encoded


@pytest.mark.parametrize('k', [4, 7, 10, 13])
def test_gray_knuth(k):
    c = Counter()
    for i in range(2 ** k):
        original = bin(i)[2:].zfill(k)
        encoded = check_encoding(original)
        c.update([encoded])
    assert (max(c.values()) == 1)


@pytest.mark.parametrize('length', [150, 200, 500, 1000])
def test_random_long_data(length):
    for _ in range(100):
        random_bytes = os.urandom(ceil(length / 8))
        original = ''.join([bin(byte)[2:] for byte in random_bytes])[:length]
        check_encoding(original)


@pytest.mark.parametrize("encoded_length, decoded_length", [
    (12, 7),
    (14, 8)
])
def test_find_decoded_length(encoded_length, decoded_length):
    assert (find_decoded_length(encoded_length) == decoded_length)
