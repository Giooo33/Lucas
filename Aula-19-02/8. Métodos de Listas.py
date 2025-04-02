#8. Métodos de Listas

# append(): Adicione o elemento 99 à lista [10, 20, 30].

my_list = [10, 20, 30]
my_list.append (99)

print(f"{my_list}")

#clear(): Limpe todos os elementos da lista [1, 2, 3, 4, 5].

my_list = [1, 2, 3, 4, 5]
my_list.clear()
print(f"{my_list}")

#copy(): Copie a lista [7, 8, 9] para uma nova lista e modifique a cópia sem alterar a original.

my_list = [7, 8, 9]
my_list_copy = my_list.copy()
my_list_copy[0] = 100
print(f"Lista original: {my_list}")
print(f"Cópia da lista: {my_list_copy}")

#count(): Conte quantas vezes o número 3 aparece na lista [1, 3, 3, 7, 3, 9].

lista = [1, 3, 3, 7, 3, 9]
print(f"O número 3 aparece {lista.count(3)} vezes na lista.")

#extend(): Una as listas [1, 2, 3] e [4, 5, 6].

lista = [1, 2, 3]
lista.extend([4, 5, 6])
print(f"{lista}")

#index(): Encontre a posição do elemento 20 na lista [5, 10, 15, 20, 25].

lista = [5, 10, 15, 20 ,25]
lista.index(20)
print(f"O elemento 20 está na posição {lista.index(20)} da lista.")

#pop(): Remova o último elemento da lista [10, 20, 30] e exiba o valor removido.

lista = [10, 20, 30]
print(f"O último elemento foi removido {lista.pop(2)}, ficando {lista}")

# remove(): Remova o primeiro 7 da lista [7, 8, 9, 7, 10].

lista = [7, 8, 9, 7, 10]
print(f"O primeiro 7 foi removido {lista.remove(7)}, ficando {lista}")

# reverse(): Inverta a lista [1, 2, 3, 4, 5].

lista = [1, 2, 3, 4, 5]
print(f"A lista invertida fica {lista.reverse()}, ficando {lista}")

# sort(): Ordene a lista [5, 3, 8, 1, 2] em ordem crescente.

lista = [5, 3, 8, 1, 2]
lista.sort()
print(f"A lista ordenada fica {lista}")

# sorted(): Exiba uma versão ordenada da lista [9, 4, 6, 2, 8] sem modificar a original.

lista = [9, 4, 6, 2, 8]
sorted(lista)
print(f"A lista ordenada fica {sorted(lista)}")
