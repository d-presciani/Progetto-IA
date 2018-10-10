# TODO Aggiungere euristica posizioni sbagliate, aggiungere switch case per calcolo eutistica
# TODO MEGA IMPORTANTE: camire come cazzo si esporta su excel
from random import randint
import time


# Funzione per stampa della griglia
def stampa(grl):
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


def conflittiVerticali(grl):
    puzz = grl
    lc = 0
    for colonna in range(4):
        massimo = -1
        for riga in range(4):
            numero = puzz[colonna+riga*4]
            rDest = numero % 4
            if numero != 0 and rDest == colonna+1:
                if numero > massimo:
                    massimo = numero
                else:
                    lc += 2
    return lc


def conflittiOrizzontali(grl):
    puzz = grl
    lc = 0
    for riga in range(4):
        massimo = -1
        for colonna in range(4):
            numero = puzz[colonna+riga*4]
            cDest = (numero-1) // 4
            if numero != 0 and cDest == riga:
                if numero > massimo:
                    massimo = numero
                else:
                    # linear conflict, one tile must move left or right to allow the other to pass by and then back up
                                # add two moves to the manhattan distance
                    lc += 2

    return lc

# Shuffle della griglia di partenza


def mescola():
    old = -1  # Variabile per la memorizzazione dell'ultimo numero mosso
    while(distanzaManhattan(griglia) < 1):
        for i in range(0, 20):
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
            # Elementi contiene tutti i numeri che circondano lo 0 e ne scelgo uno a caso
            ran = elementi[randint(0, len(elementi)-1)]
            # Ottengo l'indice del numero da muovere e dello 0
            indiceElemento = griglia.index(ran)
            indiceSpazio = griglia.index(0)
            # Inverto gli elementi
            griglia[indiceSpazio] = ran
            griglia[indiceElemento] = 0
            old = ran  # Aggiorno l'ultimo numero mosso


def espandiElemento(grid, indZero, indNum, mosse):
    global primaEsec
    global finito
    global elapsed_time
    # Inverto di posizione lo 0 e il numero passato come indAlt
    mom = list(grid)
    mom[indZero] = mom[indNum]
    mom[indNum] = 0
    # Controllo che la nuova configurazione ottenuta invertendo il numero e lo zero non sia già stata analizzata
    if mom not in frontiera and mom not in eliminati:
        # Se la nuova configurazione non è mai stata analizzata la aggiungo alla frontiera e ne calcolo la distanza di MANHATTAN
        frontiera.append(list(mom))
        temp = list(mosse)
        temp.append(mom[indZero])
        elencoMosse.append(list(temp))
        dm = distanzaManhattan(mom)
        if dm == 0:
            finito = True
            temp = list(mosse)
            temp.append(mom[indZero])
            elencoMosse.clear()
            elencoMosse.append(list(temp))
            elapsed_time = time.time() - start_time
        else:
            distanzeMNH.append(distanzaManhattan(mom))
        # Inserimento del numero mosso alla lista delle mosse da eseguire


# Funzione per espansione della frontiera di una griglia
def espandiFrontiera(grid):
    global primaEsec
    indiceZero = grid.index(0)  # Ricerca dello 0 nella griglia fornita
    posX = indiceZero % 4
    posY = indiceZero // 4
    if primaEsec:
        mosse = []  # Array per la memorizzazione delle mosse fatte
    else:
        # ottendo l'indice dell'elem
        indiceElem = frontiera.index(grid)
        # Recupero elenco mosse fatte per arrivare a questa configurazione
        mosse = elencoMosse[indiceElem]

    # Inserimento di tutte le possibili mosse nella frontiera partendo dall'attuale configurazione
    # Zero nella prima colonna, inserisco in frontiera il numero a destra dello zero
    if posX == 0:
        espandiElemento(grid, indiceZero, indiceZero+1, mosse)
    # Zero nelle colonne centrale, inserisco in frontiera il numero a sinistra e quello a destra dello zero
    elif posX > 0 and posX < 3:
        espandiElemento(grid, indiceZero, indiceZero+1, mosse)
        espandiElemento(grid, indiceZero, indiceZero-1, mosse)
    # Zero nel'ultima colonna, inserisco in frontiera il numero a sinistra dello zero
    elif posX == 3:
        espandiElemento(grid, indiceZero, indiceZero-1, mosse)
    # Zero nella prima riga, inserisco in frontiera il numero sotto allo zero
    if posY == 0:
        espandiElemento(grid, indiceZero, indiceZero+4, mosse)
    # Zero nelle righe centrali, inserisco in frontiera il numero sopra e quello sotto allo zero
    elif posY > 0 and posY < 3:
        espandiElemento(grid, indiceZero, indiceZero+4, mosse)
        espandiElemento(grid, indiceZero, indiceZero-4, mosse)
    # Zero nell'ultima' riga, inserisco in frontiera il numero sopra allo zero
    elif posY == 3:
        espandiElemento(grid, indiceZero, indiceZero-4, mosse)
    if not primaEsec and not finito:
        # Elimino dalla frontiera la configurazione appena analizzata (elimino la relativa distanza di Manhattan e l'elenco mosse)
        indiceElim = frontiera.index(grid)
        del frontiera[indiceElim]
        del distanzeMNH[indiceElim]
        del elencoMosse[indiceElim]
        # Aggiungo la configurazione eliminata a quelle eleminate per controllo di non ripetizione
        eliminati.append(list(grid))
    else:
        primaEsec = False


for iterazione in range(20):
    print("\n\nIterazione #", iterazione)
    # Variabili
    frontiera = []  # La frontiera contiene tutte le configurazioni da esplorare
    eliminati = []  # Elenco configurazioni eliminate
    distanzeMNH = []  # Lista di distanze di Manhattan legate agli elementi nella frontiera
    elencoMosse = []  # Lista contenente le liste delle mosse da eseguire che portano alla soluzione
    nroNodiCk = 0  # Contatore dei cicli
    finito = False  # Flag per controllo fine
    primaEsec = True  # Flag per controllo prima esecuzione

    # Generazione griglia e mescolamento
    griglia = [i for i in range(1, 16)]
    griglia.append(0)
    mescola()
    stampa(griglia)
    grigliaCopy = griglia
    print("Distanza di Manhattan iniziale: ", distanzaManhattan(griglia), "\n")

    # Inizio ricerca soluzione
    elapsed_time = 0
    start_time = time.time()
    eliminati.append(griglia)
    espandiFrontiera(griglia)
    while nroNodiCk <= 10000 and not finito:
        # if nroNodiCk % 1000 == 0:
        #    print("Iterazione nro: ", nroNodiCk)
        nroNodiCk += 1

        # Variabili per ricerda del minimo:
        distManMin = distanzeMNH[0] + \
            conflittiVerticali(frontiera[0]) + conflittiOrizzontali(frontiera[0])
        indiceMin = [0]

        # Ricerca dell'elemento con distanza di Manhattan greedy
        for i in range(1, len(frontiera)):
            valEuristica = distanzeMNH[i] + \
                conflittiVerticali(frontiera[i]) + conflittiOrizzontali(frontiera[i])
            if distanzeMNH[i] < distManMin:
                indiceMin.clear()
                distManMin = distanzeMNH[i]
                indiceMin.append(i)
            elif distanzeMNH[i] == distManMin:
                indiceMin.append(i)

        if not finito:
            espandiFrontiera(frontiera[indiceMin[randint(0, len(indiceMin)-1)]])

    if finito:
        mosse = elencoMosse[0]
        print("\nSOLUZIONE MANHATTAN GREEDY")
        print("E' stata trovata una soluzione in ", nroNodiCk, "passi")
        print("Nunero di mosse da eseguire: ", len(mosse))
        print("Tempo impiegato: ", elapsed_time)
        print("Elenco mosse:\n", mosse)
    else:
        print("Soluzione non trovata in 100000 passi")

    print("\n\n")

    # Reset delle variabili per ripetizione con euristica diversa
    frontiera = []
    eliminati = []
    distanzeMNH = []
    elencoMosse = []
    nroNodiCk = 0
    finito = False
    primaEsec = True
    griglia = grigliaCopy
    start_time = time.time()
    eliminati.append(griglia)
    espandiFrontiera(griglia)

    while nroNodiCk <= 10000 and not finito:
        # if nroNodiCk % 1000 == 0:
        #    print("Iterazione nro: ", nroNodiCk)
        nroNodiCk += 1

        # Variabili per ricerda del minimo:
        distASMin = distanzeMNH[0] + len(elencoMosse[0]) + \
            conflittiVerticali(frontiera[0]) + conflittiOrizzontali(frontiera[0])
        indiceMin = [0]

        # Ricerca dell'elemento con distanza di Manhattan + A*
        for i in range(1, len(frontiera)):
            valEuristica = distanzeMNH[i] + len(elencoMosse[i]) + \
                conflittiVerticali(frontiera[i]) + conflittiOrizzontali(frontiera[i])
            if valEuristica < distASMin:
                distASMin = valEuristica
                indiceMin.clear()
                indiceMin.append(i)
            elif valEuristica == distASMin:
                indiceMin.append(i)

        if not finito:
            espandiFrontiera(frontiera[indiceMin[randint(0, len(indiceMin)-1)]])

    if finito:
        mosse = elencoMosse[0]
        print("\nSOLUZIONE MANHATTAN +A*")
        print("E' stata trovata una soluzione in ", nroNodiCk, "passi")
        print("Nunero di mosse da eseguire: ", len(mosse))
        print("Tempo impiegato: ", elapsed_time)
        print("Elenco mosse:\n", mosse)
    else:
        print("Soluzione non trovata in 100000 passi")
