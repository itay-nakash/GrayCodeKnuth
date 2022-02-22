
from sympy.combinatorics.graycode import GrayCode

def main():
    gray_codes = GrayCode(10)
    print (list(gray_codes.generate_gray()))

if __name__ == "__main__":
    main()