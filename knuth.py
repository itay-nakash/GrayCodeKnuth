import math
from math import ceil, floor, log2, log
from sympy.combinatorics.graycode import GrayCode, gray_to_bin
from scipy.special import lambertw
from collections import Counter


def number_to_base(n, b, log):
    """
    convert @n (in decimal) to base @b.
    the output is of length @log.
    """
    digits = ""
    while n:
        digits += (str(n % b))
        n //= b
    return digits[::-1].zfill(log)


def count_chars(string, alphabet_size):
    """
    @string is a string above tha alphabet {0, ..., @alphabet_size - 1}.
    return a list of size @alphabet_size.
    the i'th entry is number of appearences of i in @string.
    """
    count = [0] * alphabet_size
    for c in string:
        count[int(c)] = count[int(c)] + 1
    return count


def count_sigma(string, sigma):
    """
    return how many times @sigma appears in @string
    """
    return len([s for s in string if s == sigma])


def balance_string(string, alphabet_size):
    """
    return a balanced string of @string of length @alphabet_size * (@string length).
    balancing is done by duplicating @string @alphabet_size times and chancing the symbols cyclicly.
    """
    string = [int(c) for c in string]
    res = []
    for i in range(alphabet_size):
        res += ["".join([str((c + i) % alphabet_size) for c in string])]
    return "".join(res)


def find_replacement(greater_than_goal, goal, count_array):
    """
    find a letter to balance with.
    @greater_than_goal - boolean indicates if the letter we want to replace appears more times than we want.
    @goal - the desired number of apearences.
    @count_array - an array indicates how many times each letter appears
    """
    if greater_than_goal:
        return next(i for i, x in enumerate(count_array) if x < goal)
    else:
        return next(i for i, x in enumerate(count_array) if x > goal)


def sub_num_iterations(string_length, alphabet_size):
    """
    computes how many iterations of nested balancing is the best.
    return a tuple - the first entry is the balanced length, the second entry is number of iterations
    """
    if string_length <= alphabet_size * (math.ceil(math.log(string_length, alphabet_size)) + 1):
        return string_length * alphabet_size, 1
    cont = sub_num_iterations(alphabet_size * (math.ceil(math.log(string_length, alphabet_size)) + 1), alphabet_size)
    if string_length + cont[0] < string_length * alphabet_size:
        return string_length + cont[0], 1 + cont[1]
    return string_length * alphabet_size, 1


def num_iterations(string_length, alphabet_size):
    """
    computes how many iterations of nested balancing is the best.
    """
    return sub_num_iterations(string_length, alphabet_size)[1]


def calculate_output_length(string_length, alphabet_size):
    """
    computes the length we get after encoding a string of length @string_length.
    """
    return sub_num_iterations(string_length, alphabet_size)[0]


def sub_encode_knuth(string, alphabet_size, iterations_counter):
    """
    encode @string according to knuth's algorithm, when @string is above alphabet {0, ..., alphabet_size - 1},
    with @iterations_counter times of nested balancing
    """
    if iterations_counter == 1:  # last iteration
        return balance_string(string, alphabet_size)

    string = [int(c) for c in string]
    appearance_goal = len(string) // alphabet_size
    addition_string = []  # the string that contains the indexes and the letters we balanced with
    for sigma in range(alphabet_size - 1, -1, -1):
        sigma_count = count_sigma(string, sigma)
        sigma_replacement = sigma if sigma_count == appearance_goal else \
            find_replacement(sigma_count > appearance_goal, appearance_goal,
                             count_chars(string, alphabet_size)[:sigma + 1])
        for idx, char in enumerate(string):  # balance sigma with sigma_replacement
            if sigma_count == appearance_goal:
                addition_string += (str(sigma_replacement) +
                                    number_to_base(idx, alphabet_size, math.ceil(math.log(len(string), alphabet_size))))
                break
            if char == sigma:
                string[idx] = sigma_replacement
                sigma_count -= 1
            elif char == sigma_replacement:
                string[idx] = sigma
                sigma_count += 1

    string = [str(c) for c in string]
    return "".join(string) + sub_encode_knuth("".join(addition_string), alphabet_size,
                                              iterations_counter - 1)  # recursively encode the addition_string


def encode_knuth(string, alphabet_size):
    """
    encode @string according to knuth's algorithm, when @string is above alphabet {0, ..., alphabet_size - 1}
    """
    return sub_encode_knuth(string, alphabet_size, num_iterations(len(string), alphabet_size))


def calc_indexes(alphabet_size, orig_length):
    """
    calculates indexes for seperating the encoded strings into the algorithm levels.
    """
    indexes = [orig_length]
    for i in range(num_iterations(orig_length, alphabet_size) - 1):
        indexes += [(math.ceil(math.log(indexes[-1], alphabet_size)) + 1) * alphabet_size]
    return indexes


def split_string(string, alphabet_size, orig_length):
    """
    split @string to strings according to the algorythm levels.
    @orig_length is the length of @string before the encoding.
    """
    indexes = calc_indexes(alphabet_size, orig_length)
    strings = []
    for ind in indexes:
        strings += [string[:ind]]
        string = string[ind:]
    return strings + [string]


def sub_decode(encoded_str, index_str, alphabet_size):
    """
    decode the @encoded_str string when the indexes are @index_str.
    this function is one level of decoding.
    """
    index_str = index_str[:-(len(index_str) // alphabet_size)]
    encoded_list = [int(c) for c in encoded_str]
    for sigma in range(1,
                       alphabet_size):  # decode each letter according to the corresponding letter and index from index_str
        sigma_index = (index_str[-(len(index_str) // (alphabet_size - sigma)):])
        sigma_replacement = int(sigma_index[0])
        index = int(sigma_index[1:], base=alphabet_size)
        for i in range(index):
            if encoded_list[i] == sigma:
                encoded_list[i] = sigma_replacement
            elif encoded_list[i] == sigma_replacement:
                encoded_list[i] = sigma

        index_str = index_str[:-(len(index_str) // (alphabet_size - sigma))]

    return "".join([str(c) for c in encoded_list])


def decode_knuth(string, alphabet_size, orig_length):
    """
    decode @string according to knuth's algorythm.
    @orig_length is the length of @string before the encoding.
    """
    strings = split_string(string, alphabet_size, orig_length)
    strings = strings[:-1]

    for i in range(len(strings) - 1, 0, -1):  # iteratively decode the string according to the algortihm.
        strings[i - 1] = sub_decode(strings[i - 1], strings[i], alphabet_size)

    return strings[0]


def add_balance_bit(encoded_string, counter):
    if 0 <= (counter['1'] - counter['0']) <= 2:
        return encoded_string + '0'
    elif 1 <= (counter['0'] - counter['1']) <= 2:
        return encoded_string + '1'


def encode_gray_knuth(string):
    gray_len = ceil(log2(len(string) + 1))
    gray_code = GrayCode(gray_len)
    encoded_data_prefix = ''
    for i, suffix in zip(range(len(string) + 1), gray_code.generate_gray()):
        if i > 0:
            encoded_data_prefix += str(1 - int(string[i - 1]))
        encoded_data = encoded_data_prefix + string[i:]
        encoded_string = encoded_data + suffix
        counter = Counter(encoded_string)
        balanced_encoded_string = add_balance_bit(encoded_string, counter)
        if balanced_encoded_string:
            return balanced_encoded_string


def get_encoded_length(data_len):
    return data_len + ceil(log2(data_len + 1)) + 1


def find_decoded_length(encoded_length):
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
    return ''.join([str(1 - int(bit)) for bit in string[:index]]) + string[index:decoded_length]
