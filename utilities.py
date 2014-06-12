'''
Created on Jun 12, 2014

@author: dave
'''
from dragonfly import Key

def press_digits(n):
    number=str(n)
    for digit in number:
        Key(digit).execute()