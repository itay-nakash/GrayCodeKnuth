from collections import Counter
from math import ceil, log2

from sympy.combinatorics.graycode import GrayCode, gray_to_bin


def get_gray_length(n):
    """
    :param n: The length of the raw data
    :return: The length of the gray code required for indices of this data
    """
    return ceil(log2(2 * n + 1))


def get_encoded_length(data_len):
    """
    :param data_len: The length of the raw data
    :return: The length of the encoded data
    """
    return data_len + get_gray_length(data_len) + 1


def flip_bit(bit):
    """
    :param bit: '0' or '1'
    :return: '1' or '0', respectively
    """
    return str(1 - int(bit))


def flip_string(string):
    """
    Flips the given binary string - '0' to '1' and vice versa.
    :param string: String to flip.
    :return: Flipped string.
    """
    return ''.join([flip_bit(bit) for bit in string])


def get_partially_flipped_string(data, i):
    """
    Get the partially flipped data corresponding to the index i from the (i-1)th partially-flipped string.
    :param data: Data to transform.
    :param i: The index of the flip.
    :return: Partially flipped data for the i'th index.
    """
    if 0 < i <= len(data):
        data = data[:i - 1] + flip_bit(data[i - 1]) + data[i:]
    elif i > len(data):
        data = data[:i - len(data) - 1] + flip_bit(data[i - len(data) - 1]) + data[i - len(data):]
    return data


def add_balance_bit(encoded_string, counter):
    """
    Adds a balance bit (a bit that's used to compensate for the 2-jumps in the encoded word's weight throughout
    the encoding process)

    :param encoded_string: The encoded (data + gray index) string.
    :param counter: Counter for the amount of 0's and 1's in encoded_string.
    :return: encoded_string with a balance bit as a suffix, if it's possible to balance it, otherwise None.
    """
    if 0 <= (counter['1'] - counter['0']) <= 2:
        return encoded_string + '0'
    elif 1 <= (counter['0'] - counter['1']) <= 2:
        return encoded_string + '1'


def encode_gray_knuth(string):
    """
    Encodes the given binary string using GrayKnuth® algorithm.
    :param string: Data to encode.
    :return: Encoded data.
    """
    gray_len = get_gray_length(len(string))
    gray_code = GrayCode(gray_len)
    flipped_data = string
    for i, suffix in zip(range(2 * len(string) + 1), gray_code.generate_gray()):
        flipped_data = get_partially_flipped_string(flipped_data, i)
        encoded_string = flipped_data + suffix
        counter = Counter(encoded_string)
        balanced_encoded_string = add_balance_bit(encoded_string, counter)
        if balanced_encoded_string:
            return balanced_encoded_string


def find_decoded_length(encoded_length):
    """
    Finds the length of the decoded data according to the length of the encoded data.
    Implemented using a binary search, relying on the fact that the encoded length as function of the decoded length
    is increasing.
    :param encoded_length: Length of the encoded data.
    :return: Length of the decoded data.
    """
    start = 0
    end = encoded_length

    while start <= end:
        mid = (start + end) // 2
        mid_encoded_length = get_encoded_length(mid)
        if encoded_length == mid_encoded_length:
            return mid

        if encoded_length < mid_encoded_length:
            end = mid - 1
        else:
            start = mid + 1


def decode_gray_knuth(string, decoded_length=0):
    """
    Decodes the given binary string using GrayKnuth® algorithm.
    :param string: Data to decode.
    :param decoded_length: Optional. The expected length of the decoded data. If 0 - it is determined by the length
    of the encoded data.
    :return: Decoded data.
    """
    if decoded_length == 0:
        decoded_length = find_decoded_length(len(string))
    gray_index = string[decoded_length:-1]
    index = int(gray_to_bin(gray_index), 2)
    if index <= decoded_length:
        return flip_string(string[:index]) + string[index:decoded_length]
    else:
        index = index - decoded_length
        return string[:index] + flip_string(string[index:decoded_length])