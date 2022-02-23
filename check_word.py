from sympy.combinatorics.graycode import GrayCode
from math import ceil, log2

word = '0000000'
k = len(word)
gray_len = ceil(log2(k + 1))
g = GrayCode(gray_len)
has_balanced = False
for j, suffix in zip(range(k + 1), g.generate_gray()):
    w1 = sum(1 - int(bit) for bit in word[:j])
    w2 = sum(int(bit) for bit in word[j:] + suffix)
    w = w1 + w2
    new_word = ''.join([str(1 - int(bit)) for bit in word[:j]]) + word[j:]
    print(f'{new_word + suffix} {w=}')
    if abs(w - ((k + gray_len) / 2)) <= 0:
        has_balanced = True
if not has_balanced:
    print('Not balanced')