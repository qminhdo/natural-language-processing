import unittest
from mycode import *


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

class MyTests(unittest.TestCase):
    def test_hello(self):
        self.assertEqual('hello world', hello_world())

if __name__ == '__main__':
    unittest.main()

