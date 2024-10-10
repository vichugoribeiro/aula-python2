
import random
lista = [random.randint(1, 100) for _ in range (5)]

def setUP(self):
    self.lista = [10, 20, 30]
    
    
def numero_novo(self):
    self.assertIn ('novo numero')
    
def numero_remover(self):
    self.assertNotIn ('remover numero')
    
    with self.assertRaises (ValueError):
        numero_remover(self.list, 100)
    
