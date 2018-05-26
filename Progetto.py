# TODO: Modificare controllo inserimento con possibilità di sovrascrivere elenco mosse di stessa configurazione
# se uguale configurazione ma con elenco mosse minore
from random import randint


# Funzione per stampa della griglia
def stampa():
    ctr = 0
    str = ''
    print("Griglia:")
    for el in griglia:
        mom = repr(el)
        if el == 0:
            mom = ' *'
        if len(mom) == 1:
            mom = ' ' + mom
        str += mom + ' '
        ctr += 1
        if ctr % 4 == 0 and ctr != 0:
            print(str)
            str = ''
    return


def stampaEl(grl):
    ctr = 0
    str = ''
    print("Griglia:")
    for el in grl:
        mom = repr(el)
        if el == 0:
            mom = ' *'
        if len(mom) == 1:
            mom = ' ' + mom
        str += mom + ' '
        ctr += 1
        if ctr % 4 == 0 and ctr != 0:
            print(str)
            str = ''
    return


# Calcolo della distanza di Manhattan per la griglia data
def distanzaManhattan(lst):
    md = 0
    for elem in lst:
        if elem != 0:
            deltaY = abs((elem-1) // 4 - lst.index(elem) // 4)
            deltaX = abs((elem-1) % 4 - lst.index(elem) % 4)
            md += deltaX + deltaY
    return md


# Shuffle della griglia di partenza
def mescola():
    old = -1
    while(distanzaManhattan(griglia) < 20):
        for i in range(0, 500):
            elementi = []
            indice = griglia.index(0)
            posX = indice % 4
            posY = indice // 4
            if posX == 0:
                if old == -1 or griglia[indice+1] != old:
                    elementi.append(griglia[indice+1])
            elif posX > 0 and posX < 3:
                if old == -1 or griglia[indice+1] != old:
                    elementi.append(griglia[indice+1])
                if old == -1 or griglia[indice-1] != old:
                    elementi.append(griglia[indice-1])
            elif posX == 3:
                if old == -1 or griglia[indice-1] != old:
                    elementi.append(griglia[indice-1])
            if posY == 0:
                if old == -1 or griglia[indice+4] != old:
                    elementi.append(griglia[indice+4])
            elif posY > 0 and posY < 3:
                if old == -1 or griglia[indice+4] != old:
                    elementi.append(griglia[indice+4])
                if old == -1 or griglia[indice-4] != old:
                    elementi.append(griglia[indice-4])
            elif posY == 3:
                if old == -1 or griglia[indice-4] != old:
                    elementi.append(griglia[indice-4])
            ran = elementi[randint(0, len(elementi)-1)]
            indiceElemento = griglia.index(ran)
            indiceSpazio = griglia.index(0)
            griglia[indiceSpazio] = ran
            griglia[indiceElemento] = 0
            old = ran


def espandiSingolo(el, ind, indAlt, mosse):
    global primaEsec
    mom = list(el)
    mom[ind] = mom[indAlt]
    mom[indAlt] = 0
    if mom not in frontiera and mom not in eliminati:
        frontiera.append(list(mom))
        distanzeMNH.append(distanzaManhattan(mom))
        temp = list(mosse)
        temp.append(mom[ind])
        elencoMosse.append(list(temp))


# Funzione per espansione della frontiera
def espandiFrontiera(el):
    global primaEsec
    indice = el.index(0)
    posX = indice % 4
    posY = indice // 4
    if primaEsec:
        mosse = []
    else:
        indiceElem = frontiera.index(el)
        mosse = elencoMosse[indiceElem]
    if posX == 0:
        espandiSingolo(el, indice, indice+1, mosse)
    elif posX > 0 and posX < 3:
        espandiSingolo(el, indice, indice+1, mosse)
        espandiSingolo(el, indice, indice-1, mosse)
    elif posX == 3:
        espandiSingolo(el, indice, indice-1, mosse)
    if posY == 0:
        espandiSingolo(el, indice, indice+4, mosse)
    elif posY > 0 and posY < 3:
        espandiSingolo(el, indice, indice+4, mosse)
        espandiSingolo(el, indice, indice-4, mosse)
    elif posY == 3:
        espandiSingolo(el, indice, indice-4, mosse)
    if not primaEsec:
        indiceElim = frontiera.index(el)
        del frontiera[indiceElim]
        del distanzeMNH[indiceElim]
        del elencoMosse[indiceElim]
        eliminati.append(list(el))
    else:
        primaEsec = False


# Variabili
frontiera = []  # La frontiera contiene tutte le configurazioni da esplorare
eliminati = []  # Elenco configurazioni eliminate
distanzeMNH = []  # Lista di distanze di Manhattan legate agli elementi nella frontiera
elencoMosse = []  # Lista contenente le mosse da eseguire che portano alla soluzione
nroNodiCk = 0
finito = False
primaEsec = True

# Generazione griglia e mescolamento
griglia = [i for i in range(1, 16)]
griglia.append(0)
mescola()
stampa()
print("Distanza di Manhattan iniziale: ", distanzaManhattan(griglia), "\n")
eliminati.append(griglia)
espandiFrontiera(griglia)
while nroNodiCk <= 100000 and not finito:
    if nroNodiCk % 1000 == 0:
        print("Iterazione nro: ", nroNodiCk)
    nroNodiCk += 1
    indiceMin = distanzeMNH.index(min(distanzeMNH))
    if distanzeMNH[indiceMin] == 0:
        finito = True
    else:
        espandiFrontiera(frontiera[indiceMin])
if finito:
    mosse = elencoMosse[distanzeMNH.index(min(distanzeMNH))]
    print("E' stata trovata una soluzione in ", nroNodiCk, "passi")
    print("Nunero di mosse da eseguire: ", len(mosse))
    print("Elenco mosse:\n", mosse)
else:
    print("Soluzione non trovata in 100000 passi")
