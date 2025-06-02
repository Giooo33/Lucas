# Calculadora de Média de Notas
# Neste ´rogrma é pedido ao usuário a quantidade de notas que ele
# deseja inserir, e em sguida ele insere as notas dentro de vetor chamado
# notas. Posteriormente, dentro de um laço de repetição, o programa
# pede as notas e as adiciona ao vetor. Ao final, o programa calcula a 
# média das notas e exibe o resultado formatado com 2 casas decimais.

def main ():
    print("Calculadora de Média de Notas")
    quantidade = int(input("Quantas notas você deseja inserir: "))
    notas = []

    for i in range(quantidade):
        nota = float(input(f"Digite a {i + 1}ª nota: "))
        notas.append(nota) # Adiciona a nota à lista (append adiciona um elemento ao final da lista)
        media = sum(notas) / quantidade # Um soma todos os elementos da lista notas e divide pela quantidade
    
    print(f"A média das {quantidade} notas é : {media:.2f}") # O .2f formata a média com 2 casas decimais

if __name__ == "__main__":
    main()  