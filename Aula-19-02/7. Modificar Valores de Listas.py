#7. Modificar Valores de Listas

#Dada a lista [1, 2, 3, 4, 5], multiplique todos os elementos por 2.

lista = [1, 2, 3, 4, 5]
mult = []

for multiplicacao in lista:

    mult.append(multiplicacao * 2)

print(mult) 

#Substitua todos os números maiores que 50 por 50 na lista [10, 20, 60, 80, 100].

lista = [10, 20, 60, 80, 100]
maiores = []

for numero in lista:

    if numero > 50:
        lista [lista.index(numero)] = 50
        
print(lista)


