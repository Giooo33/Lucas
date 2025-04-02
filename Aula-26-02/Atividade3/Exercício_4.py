# Exercício_4

class Funcionario:
    def __init__(self, nome, salario,):
        self.nome = input(nome)
        self.salario = int(input(salario))

    def exibir_informacoes (self):
        print(f"O nome do usuário é {self.nome} e seu salário é {self.salario}")

class Gerente (Funcionario):
    def __init__(self, bonus):
        self.bonus = int (input (bonus))
    
    def exibir_informacoes(self):
        return super().exibir_informacoes()
    print("O bônus é {self.bonus}")

cliente_1 = Funcionario (input ("Insira o nome do funcionário: "), int (input ("Insira o sálario do funcionário: ")))



