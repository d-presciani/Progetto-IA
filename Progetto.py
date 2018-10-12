# TODO Aggiungere euristica posizioni sbagliate, aggiungere switch case per calcolo eutistica
# TODO MEGA IMPORTANTE: camire come cazzo si esporta su excel
from random import randint
import time

# Var globali
maxCicli = 5000
dimensione = 4  # Numero di elementi per riga (numero di elementi totali = dimensione^2 -1)


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
        if ctr % dimensione == 0 and ctr != 0:
            print(str)
            str = ''
    return


# Calcolo del numero di elementi fuori posizione
def fuoriposto(grl):
    fp = 0
    for ind in range(dimensione*dimensione):
        if grl[ind] != 0 and grl[ind]-1 != ind:
            fp += 1
    return fp


# Calcolo della distanza di Manhattan per la griglia data
def distanzaManhattan(lst):
    md = 0
    for elem in lst:
        if elem != 0:
            deltaY = abs((elem-1) // dimensione - lst.index(elem) // dimensione)
            deltaX = abs((elem-1) % dimensione - lst.index(elem) % dimensione)
            md += deltaX + deltaY
    return md


# Calcolo dei conflitti verticali
def conflittiVerticali(grl):
    puzz = grl
    lc = 0
    for colonna in range(dimensione):
        massimo = -1
        for riga in range(dimensione):
            numero = puzz[colonna+riga*dimensione]
            rDest = numero % dimensione
            if numero != 0 and rDest == colonna+1:
                if numero > massimo:
                    massimo = numero
                else:
                    lc += 2
    return lc


# Calcolo dei conflitti orizzontali
def conflittiOrizzontali(grl):
    puzz = grl
    lc = 0
    for riga in range(dimensione):
        massimo = -1
        for colonna in range(dimensione):
            numero = puzz[colonna+riga*dimensione]
            cDest = (numero-1) // dimensione
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
        for i in range(0, 25):
            elementi = []
            indice = griglia.index(0)
            posX = indice % dimensione
            posY = indice // dimensione
            if posX == 0:
                if old == -1 or griglia[indice+1] != old:
                    elementi.append(griglia[indice+1])
            elif posX > 0 and posX < dimensione-1:
                if old == -1 or griglia[indice+1] != old:
                    elementi.append(griglia[indice+1])
                if old == -1 or griglia[indice-1] != old:
                    elementi.append(griglia[indice-1])
            elif posX == dimensione-1:
                if old == -1 or griglia[indice-1] != old:
                    elementi.append(griglia[indice-1])
            if posY == 0:
                if old == -1 or griglia[indice+dimensione] != old:
                    elementi.append(griglia[indice+dimensione])
            elif posY > 0 and posY < dimensione-1:
                if old == -1 or griglia[indice+dimensione] != old:
                    elementi.append(griglia[indice+dimensione])
                if old == -1 or griglia[indice-dimensione] != old:
                    elementi.append(griglia[indice-dimensione])
            elif posY == dimensione-1:
                if old == -1 or griglia[indice-dimensione] != old:
                    elementi.append(griglia[indice-dimensione])
            # Elementi contiene tutti i numeri che circondano lo 0 e ne scelgo uno a caso
            ran = elementi[randint(0, len(elementi)-1)]
            # Ottengo l'indice del numero da muovere e dello 0
            indiceElemento = griglia.index(ran)
            indiceSpazio = griglia.index(0)
            # Inverto gli elementi
            griglia[indiceSpazio] = ran
            griglia[indiceElemento] = 0
            old = ran  # Aggiorno l'ultimo numero mosso


# Generazione nuova griglia e calcolo distanza Manhattan
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
    posX = indiceZero % dimensione
    posY = indiceZero // dimensione
    if primaEsec:
        mosse = []  # Array per la memorizzazione delle mosse fatte
    else:
        # Ottendo l'indice dell'elem
        indiceElem = frontiera.index(grid)
        # Recupero elenco mosse fatte per arrivare a questa configurazione
        mosse = elencoMosse[indiceElem]

    # Inserimento di tutte le possibili mosse nella frontiera partendo dall'attuale configurazione
    # Zero nella prima colonna, inserisco in frontiera il numero a destra dello zero
    if posX == 0:
        espandiElemento(grid, indiceZero, indiceZero+1, mosse)
    # Zero nelle colonne centrale, inserisco in frontiera il numero a sinistra e quello a destra dello zero
    elif posX > 0 and posX < (dimensione-1):
        espandiElemento(grid, indiceZero, indiceZero+1, mosse)
        espandiElemento(grid, indiceZero, indiceZero-1, mosse)
    # Zero nel'ultima colonna, inserisco in frontiera il numero a sinistra dello zero
    elif posX == (dimensione-1):
        espandiElemento(grid, indiceZero, indiceZero-1, mosse)
    # Zero nella prima riga, inserisco in frontiera il numero sotto allo zero
    if posY == 0:
        espandiElemento(grid, indiceZero, indiceZero+dimensione, mosse)
    # Zero nelle righe centrali, inserisco in frontiera il numero sopra e quello sotto allo zero
    elif posY > 0 and posY < (dimensione-1):
        espandiElemento(grid, indiceZero, indiceZero+dimensione, mosse)
        espandiElemento(grid, indiceZero, indiceZero-dimensione, mosse)
    # Zero nell'ultima' riga, inserisco in frontiera il numero sopra allo zero
    elif posY == (dimensione-1):
        espandiElemento(grid, indiceZero, indiceZero-dimensione, mosse)
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


# Main
for iterazione in range(1):
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
    griglia = [i for i in range(1, dimensione*dimensione)]
    griglia.append(0)
    mescola()
    stampa(griglia)
    grigliaCopy = griglia
    print("Distanza di Manhattan iniziale: ", distanzaManhattan(griglia), "\n")
    # Inizio
    # 0 Celle fuori posto
    # 1 Manhattan
    # 2 Manhattan + inversioni
    # 3 A* (numero passi sluzione + Manhattan + inversioni)
    for euristica in range(4):
        # Reset delle variabili per ripetizione con euristica diversa
        frontiera = []
        eliminati = []
        distanzeMNH = []
        elencoMosse = []
        nroNodiCk = 0
        finito = False
        primaEsec = True
        griglia = grigliaCopy
        start_time = time.time()  # Variabile per calcolo tempo esecuzione
        eliminati.append(griglia)
        espandiFrontiera(griglia)
        while nroNodiCk <= maxCicli and not finito:
            # Numero massimo di stati esplorabili = 5000
            nroNodiCk += 1

            # Variabili per ricerda del minimo:
            indiceMin = []
            indiceMin.append(0)
            if euristica == 0:
                valEurMin = fuoriposto(frontiera[0])

            # 1 Manhattan
            elif euristica == 1:
                valEurMin = distanzeMNH[0]

                # 2 Manhattan + inversioni
            elif euristica == 2:
                valEurMin = distanzeMNH[0] + conflittiVerticali(
                    frontiera[0]) + conflittiOrizzontali(frontiera[0])

            # 3 A* (numero passi sluzione + Manhattan + inversioni)
            elif euristica == 3:
                valEurMin = distanzeMNH[0] + len(elencoMosse[0]) + \
                    conflittiVerticali(frontiera[0]) + conflittiOrizzontali(frontiera[0])

            for i in range(1, len(frontiera)):
                # 0 Celle fuori posto
                if euristica == 0:
                    valEuristica = fuoriposto(frontiera[i])

                # 1 Manhattan
                elif euristica == 1:
                    valEuristica = distanzeMNH[i]

                    # 2 Manhattan + inversioni
                elif euristica == 2:
                    valEuristica = distanzeMNH[i] + conflittiVerticali(
                        frontiera[i]) + conflittiOrizzontali(frontiera[i])

                # 3 A* (numero passi sluzione + Manhattan + inversioni)
                elif euristica == 3:
                    valEuristica = distanzeMNH[i] + len(elencoMosse[i]) + \
                        conflittiVerticali(frontiera[i]) + conflittiOrizzontali(frontiera[i])

                # Confronto nuovo valore euristica con valore minimo precedente
                if valEuristica < valEurMin:
                    valEurMin = valEuristica
                    indiceMin.clear()
                    indiceMin.append(i)
                elif valEuristica == valEurMin:
                    indiceMin.append(i)

            if not finito:
                espandiFrontiera(frontiera[indiceMin[randint(0, len(indiceMin)-1)]])

        if euristica == 0:
            print("\n\nSOLUZIONE CELLE FUORI POSTO")

        # 1 Manhattan
        elif euristica == 1:
            print("\n\nSOLUZIONE MANHATTAN")

            # 2 Manhattan + inversioni
        elif euristica == 2:
            print("\n\nSOLUZIONE MANHATTAN + INVERSIONI")

        # 3 A* (numero passi sluzione + Manhattan + inversioni)
        elif euristica == 3:
            print("\n\nSOLUZIONE A* + MANHATTAN + INVERSIONI")
        if finito:
            mosse = elencoMosse[0]
            # 0 Celle fuori posto
            print("E' stata trovata una soluzione in ", nroNodiCk, "passi")
            print("Nunero di mosse da eseguire: ", len(mosse))
            print("Tempo impiegato: ", elapsed_time)
            print("Elenco mosse:\n", mosse)
        else:
            print("Soluzione non trovata in ", maxCicli, " passi")
