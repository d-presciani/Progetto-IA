a = 7
b = 2

risFlot = a / b
risInt = a//b  # Il doppio diviso restituisce il risultato intero

print("RisFloat: ", risFlot)
print("RisInt: ", risInt)

# Prova liste

lista = []

listaMom = []
for i in range(1, 6):
    listaMom.append(i)

for i in range(0, len(listaMom)):
    print(listaMom[i])
print(len(listaMom))
print(listaMom)

"""
lista.append(list(listaMom))

listaMom.clear()
for i in range(1, 7):
    listaMom.append(i)

lista.append(list(listaMom))

print(lista)

print([1, 2, 3, 4, 5] in lista)

listaMom.append(8)
"""

"""

print(listaMom not in lista)

print(lista)

listaVuota = []

listaNV = [1, 2, 3, 4, 5]

print(6 not in listaNV)

print("Lista iniziale: ", listaNV)

print("Lunghezza lista: ", len(listaNV))

listaNV.append(6)

print("Lista post append: ", listaNV)

print("Ultimo elemento della lista: ", listaNV.pop())

print("Status lista post pop: ", listaNV)

print("Pop del secondo elemento della lista (indice 1): ", listaNV.pop(1))

print("Status lista post pop: ", listaNV)

inVal = input("Digitare qualcosa: ")

print("Il qualcosa appena digitato: ", inVal)

if True:
    print("Caso true")
elif False:
    print("Caso false")

# Promemoria si scrive elif...
"""
