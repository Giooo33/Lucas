#Exercício 1

class Carro:
    def __init__(self, marca, modelo, ano, cor):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor

    def correndo (self):
        print("O carro esta em movimento.")
        self.correndo = True

    def parado (self):
        print("O carro esta parado.")
        self.parado =False

    def buzina (self):
        print("Bi-bi-bi.")
        self.buzina = True

carro_1 = Carro ("Ford", "Licoln", 2023, "laranja")
carro_2 = Carro ("BMW", "Mini", 2022, "pérola")

print(f"O primeiro carro é da marca {carro_1.marca}, do modelo {carro_1.modelo}, do ano {carro_1.ano} e da cor {carro_1.cor}")
print(f"O segundo carro é da marca {carro_2.marca}, do modelo {carro_2.modelo}, do ano {carro_2.ano} e da cor {carro_2.cor}")

carro_2.correndo()
carro_1.buzina()
carro_1.parado()
carro_2.buzina()
