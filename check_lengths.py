#!/usr/bin/python3.8
import sys
from math import log2, ceil
from sympy.combinatorics.graycode import GrayCode

k = int(sys.argv[1]) if len(sys.argv) > 1 else 18
gray_len = ceil(log2(k + 1))
print(f"{k=}, {gray_len=}")
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
