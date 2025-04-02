# Exercício_3

class Animal:
    def __init__(self, emitirSom):
        self.emitirSom = emitirSom

        def emitirSom (self):
            print("O som do animal.")
        

class Cachorro(Animal):
    def emitirSom (self):
        print("Au-au-auuuuuuuuuu")

class Gato(Animal):
    def emitirSom (self):
        print("Miau-miau-danonenonenone")

animal_1 = Cachorro()
animal_2 = Gato()

print(f"{animal_1.emitirSom()}")