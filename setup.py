from setuptools import setup

setup(
    name='gray_knuth',
    version='0.1.0',
    description='Implementation of binary Knuth algorithm using Gray Code indices',
    author='Itay Nakash, Yuval Goldberg',
    requires=[
        'sympy',
        'pytest'
    ]
)