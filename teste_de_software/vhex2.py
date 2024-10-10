def valida_senha(senha):
    return len (senha) >= 8 and any(char.isdigit() for char in senha)

import unittest
class TestValidaSenha(unittest.TestCase):
    def test_senha_valida(self):
        self.assertTrue(valida_senha('senha123'))
    def test_senha_curta(self):
        self.assertFalse(valida_senha('curta'))
    def test_senha_sem_numero(self):
        self.assertFalse(valida_senha('semnumero'))
        
if __name__ =='__main__':
    unittest.main()