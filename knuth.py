from math import ceil, floor, log2, log
from sympy.combinatorics.graycode import GrayCode, gray_to_bin
from scipy.special import lambertw
from collections import Counter


def add_balance_bit(encoded_string, counter):
    if 0 <= (counter['1'] - counter['0']) <= 2:
        return encoded_string + '0'
    elif 1 <= (counter['0'] - counter['1']) <= 2:
        return encoded_string + '1'


def encode_gray_knuth(string):
    gray_len = ceil(log2(2 * len(string) + 1))
    gray_code = GrayCode(gray_len)
    encoded_data_prefix = ''
    for i, suffix in zip(range(2 * len(string) + 1), gray_code.generate_gray()):
        if i <= len(string):
            if i > 0:
                encoded_data_prefix += str(1 - int(string[i - 1]))
            encoded_data = encoded_data_prefix + string[i:]
        else:
            encoded_data = string[:i - len(string)] + encoded_data_prefix[i - len(string):]
        encoded_string = encoded_data + suffix
        counter = Counter(encoded_string)
        balanced_encoded_string = add_balance_bit(encoded_string, counter)
        if balanced_encoded_string:
            return balanced_encoded_string


def get_encoded_length(data_len):
    return data_len + ceil(log2(2 * data_len + 1)) + 1


def find_decoded_length(encoded_length):
    # doesn't work with the new calculation
    approx_len = (lambertw(log(2) * 2 ** encoded_length) / log(2)) - 1
    approx_len = floor(approx_len.real)
    while get_encoded_length(approx_len) < encoded_length:
        approx_len += 1
    while get_encoded_length(approx_len) > encoded_length:
        approx_len -= 1
    return approx_len


def find_decoded_length2(encoded_length):
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
    if decoded_length == 0:
        decoded_length = find_decoded_length2(len(string))
    gray_index = string[decoded_length:-1]
    index = int(gray_to_bin(gray_index), 2)
    if index <= decoded_length:
        return ''.join([str(1 - int(bit)) for bit in string[:index]]) + string[index:decoded_length]
    else:
        index = index - decoded_length
        return string[:index] + ''.join([str(1 - int(bit)) for bit in string[index:decoded_length]])
