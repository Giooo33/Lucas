#Crie um progrma onde João informe: cor, modelo, ano e valor da bicicleta vendida.
#Uma bicicleta pode: buzinar, parar e correr. Adicione esses comportamentos.

#O 'self' é uma referencia ao objeto.

#O objeto (self) seria os móveis e comodos da casa e a 'class' seria a casa em si. 

class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor 
        self.modelo = modelo
        self.ano = ano
        self.valor = valor

    def buzinar(self):
        print("Pim-Pim-Pim")
        self.buzinar = True

    def parada(self):
        print("A bicicleta parou")
        self.parada = False

    def correr(self):
        print("A bicicleta está em movimento")
        self.correr = True

    def __str__(self):
        return f"Bicicleta: modelo: {self.modelo} cor: {self.cor} ano: {self.ano} valor: {self.valor}"
    #Uma opção para mostrar os objetos atribuidos a classe.

bicicleta_1 = Bicicleta ("vermelha" , "modelo de estrada" , 2017, 1500.0)
bicicleta_2 = Bicicleta ("Verde" , "modelo de montanha" , 2022, 3500.0)

bicicleta_2.buzinar()
bicicleta_1.correr()
bicicleta_2.parada()
Bicicleta.buzinar(bicicleta_1)

print (f"Cor: {bicicleta_1.cor}")
print (f"Modelo: {bicicleta_1.modelo}")
print (f"Ano: {bicicleta_1.ano}")
print (f"Valor: {bicicleta_1.valor}")

print (f"Cor: {bicicleta_2.cor}")
print (f"Modelo: {bicicleta_2.modelo}")
print (f"Ano: {bicicleta_2.ano}")
print (f"Valor: {bicicleta_2.valor}")  



