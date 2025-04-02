entrada = input("Digite os números: ")
print(entrada)

def soma_tupla (tupla):
    return sum(tupla)

elementos = tuple (map (int, entrada .split())) # Para converter a tupla em inteiro
resultado = soma_tupla(elementos)

print(f"A soma desses números é {resultado}")



