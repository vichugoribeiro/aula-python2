def soma (a, b):
    return a + b

import unittest

class TestSoma(unittest.TestCase):
    def test_soma_positivos(self):
        self.assertEqual(soma(1, 2), 3)
        
    def test_soma_negativos(self):
        self.assertEqual(soma(-1, -1), -2)
        
    def test_soma_zero(self):
        self.assertEqual(soma(0, 0), 0)
        
if __name__ == '__main__':
    unittest.main()