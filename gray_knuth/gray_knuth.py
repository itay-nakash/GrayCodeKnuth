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
    :param string: Data to encode (represented as a binary string).
    :type string: str
    :return: Encoded data.
    :rtype: str
    """
    validate_input(string)
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
    :param encoded_length: Length of the encoded data. (as a number and not a binary string)
    :return: Length of the decoded data. (as a number and not a binary string)
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
    :param string: Data to decode. (as a GrayKnuth binary string)
    :type string: str
    :param decoded_length: Optional. The expected length of the decoded data. If 0 - it is determined by the length
    of the encoded data.
    :type decoded_length: int
    :return: Decoded data. (as a binary string)
    :rtype: str
    """
    validate_input(string)
    if decoded_length == 0:
        decoded_length = find_decoded_length(len(string))
    gray_index = string[decoded_length:-1]
    index = int(gray_to_bin(gray_index), 2)
    if index <= decoded_length:
        return flip_string(string[:index]) + string[index:decoded_length]
    else:
        index = index - decoded_length
        return string[:index] + flip_string(string[index:decoded_length])


def validate_input(input_string):
    for c in input_string:
        if c not in ['0', '1']:
            raise Exception("The input should be binary string, the char {} is illegal".format(str(c)))


def encode_gray_knuth_from_file(filename):
    """
    Encodes binary string from a file, using GrayKnuth® algorithm.
    :param filename: a path to file that contains the Data to encode (a number represented in binary format).
    :type filename: str
    :return: Encoded data.
    :rtype: str
    """
    with open(filename, 'r') as f:
        return encode_gray_knuth(f.read())


def encode_gray_knuth_to_file(string, filename):
    """
    Encodes binary string to a file, using GrayKnuth® algorithm.
    :param string: Data to encode (represented as a binary string).
    :type string: str
    :param filename: a path to create the file that will contain the encoded string.
    :type filename: str
    :return: None
    """
    with open(filename, 'w') as f:
        f.write(encode_gray_knuth(string))


def decode_gray_knuth_from_file(filename):
    """
    Decodes the given binary string from a file using GrayKnuth® algorithm.
    :param filename: a path to the file that contains the encoded string.
    :type filename: str
    :return: None
    """
    with open(filename, 'r') as f:
        return decode_gray_knuth(f.read())


def decode_gray_knuth_to_file(string, filename, decoded_length=0):
    """
    Decodes the given binary string to a file using GrayKnuth® algorithm.
    :param string: Data to decode. (as a GrayKnuth binary string)
    :type string: str
    :param decoded_length: Optional. The expected length of the decoded data. If 0 - it is determined by the length
    of the encoded data.
    :type decoded_length: int
    :param filename: a path to create the file that will contain the decoded string.
    :type filename: str
    :return: None
    """
    decoded_word = decode_gray_knuth(string, decoded_length)
    with open(filename, 'w') as f:
        f.write(decoded_word)
