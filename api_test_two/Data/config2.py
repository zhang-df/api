import pytest
from testdata.config1 import Abc


class A:
    def __init__(self):
        self.a = dir(Abc())

    def abc(self):
        return [a for a in dir(A) if not a.startswith('__')]


# print(A().abc())
def abc(login_null):
    print(login_null)

def bc():
    abc()


if __name__ == '__main__':
    pytest.main(['-q', 'config2.py'])
