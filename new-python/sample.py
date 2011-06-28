import import1, import2, import3
from multipleimport import a, b, c
from starimport import *

a = 1
a = 'asdf'
b = a

c = (1, 'asdf', a)
d, e, f = 1, 'asdf', c

def test(): pass
def test(again): pass

def multiline(arg1, arg2,
				arg3_should_be_on_another_line): pass