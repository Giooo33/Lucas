# Exercício_2

class Conta_Bancaria:
    def __init__(self, titular):
        self.titular = input(titular)
        self.saldo = 0

#O saldo estamos determinando ao contrário do titular que VAI SER DEFINIDO.

    def depositar (self):
        valor = float (input ("Insira o valor a ser depositado: "))
        print(valor)
        self.saldo += valor

    def sacar (self):
        valor = float (input ("Insira o valor a ser sacado: "))
        print(valor)

        if valor <= self.saldo:
            self.saldo -= valor

        else:
            print("Saldo insuficiente para o saque")

    def exibir_saldo (self):
        print(f"Saldo atual {self.saldo}")

cliente_1 = Conta_Bancaria (input("Insira o nome do titular: "))

#Vai ser adicionadp um valor a variável titular neste bloco.

cliente_1.depositar()
cliente_1.sacar()
cliente_1.exibir_saldo()

