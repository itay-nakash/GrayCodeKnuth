from math import log2, ceil
from sympy.combinatorics.graycode import GrayCode

k = 18
gray_len = ceil(log2(k + 1))
print(f"k={k}, gray_len={gray_len}")
for i in range(2**k):
    word = bin(i)[2:].zfill(k)
    g = GrayCode(gray_len)
    has_balanced = False
    for j, suffix in zip(range(k + 1), g.generate_gray()):
        w1 = sum(1 - int(bit) for bit in word[:j])
        w2 = sum(int(bit) for bit in word[j:] + suffix)
        w = w1 + w2
        if abs(w - ((k + gray_len) / 2)) <= 1:
            has_balanced = True
    if not has_balanced:
        print(word)
