# TODO controllo correttezza con distanza di manhattan == 0
# TODO Ricontrollare codice che sembra parecchio sbagliato
from random import randint
import time

# Var globali
maxCicli = 5000
dimensione = 4  # Numero di elementi per riga (numero di elementi totali = dimensione^2 -1)
elapsed_time = 0
file = open("risultati.txt", "w")


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


# Calcolo della distanza di Manhattan per la griglia data
def distanzaManhattan(lst):
    md = 0
    for elem in lst:
        if elem != 0:
            deltaY = abs((elem-1) // dimensione - lst.index(elem) // dimensione)
            deltaX = abs((elem-1) % dimensione - lst.index(elem) % dimensione)
            md += deltaX + deltaY
    return md


# Shuffle della griglia di partenza
def mescola():
    old = -1  # Variabile per la memorizzazione dell'ultimo numero mosso
    while(distanzaManhattan(griglia) < 1):
        for i in range(0, 100):
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


# Funzione per controllo se elemento da inserire va bene
def ckInserimento(val):
    if(len(elencoMosse) == 0):
        return True
    else:
        # Controllo elemento diverso dall'ultimo iserito nella frontiera
        if elencoMosse[-1] == val:
            return False
        else:
            return True


# TODO RIVEDERE
# Funzione per espansione della frontiera
def espandiFrontiera():
    frontiera.append(0)  # Lo 0 viene utilizzato per segnare i livelli
    indice = griglia.index(0)
    posX = indice % dimensione
    posY = indice // dimensione
    if posX == 0:
        if(ckInserimento(griglia[indice+1])):
            frontiera.append(griglia[indice+1])
    elif posX > 0 and posX < (dimensione-1):
        if(ckInserimento(griglia[indice+1])):
            frontiera.append(griglia[indice+1])
        if(ckInserimento(griglia[indice-1])):
            frontiera.append(griglia[indice-1])
    elif posX == (dimensione-1):
        if(ckInserimento(griglia[indice-1])):
            frontiera.append(griglia[indice-1])
    if posY == 0:
        if(ckInserimento(griglia[indice+dimensione])):
            frontiera.append(griglia[indice+dimensione])
    elif posY > 0 and posY < (dimensione-1):
        if(ckInserimento(griglia[indice+dimensione])):
            frontiera.append(griglia[indice+dimensione])
        if(ckInserimento(griglia[indice-dimensione])):
            frontiera.append(griglia[indice-dimensione])
    elif posY == (dimensione-1):
        if(ckInserimento(griglia[indice-dimensione])):
            frontiera.append(griglia[indice-dimensione])
    global livello
    livello += 1
    return


# TODO RISCRIVERE EXNOVO
# Generazione griglia e shuffle
'''
griglia = [i for i in range(1, dimensione*dimensione)]
griglia.append(0)
mescola()
'''
griglia = [1,  9,  4,  6, 11, 12,  2,  7,  10, 13,  5, 14, 0,  3, 15,  8]
stampa(griglia)
print("Distanza manhattan: ", distanzaManhattan(griglia))
grigliaCopy = griglia
file.write("Prof NodiEspl Tempo\n")

# Variabili
maxProfLim = 17


for maxProf in range(1, maxProfLim):
    print("Prof max: ", maxProf)
    maxProf+1
    griglia = grigliaCopy
    frontiera = []
    elencoMosse = []
    livello = 0  # Variabile per memorizzazione livello
    finito = False
    nroNodiCk = 0
    start_time = time.time()
    # Main
    # Inizialmente inserisco tutti gli elementi limitrofi a 0 nella frontiera
    espandiFrontiera()
    # Fino a quando non ho finito gli elementi nella frontiera oppure non ho trovato una soluzione
    while len(frontiera) != 0 and not finito:
        # Eseguo il movimento di uno degli elementi della Frontiera se questo non mi porta l'albero ad una profondità maggiore della massima
        if livello <= maxProf:
            elem = frontiera.pop()
            # Se l'elemento è uno zero allora riduco di uno la profondità
            if elem == 0:
                livello -= 1
            else:
                nroNodiCk += 1
                indiceElemento = griglia.index(elem)
                indiceSpazio = griglia.index(0)
                griglia[indiceSpazio] = elem
                griglia[indiceElemento] = 0
                elencoMosse.append(elem)
                # Dopo aver mosso una casella controllo di non aver trovato una soluzione
                if distanzaManhattan(griglia) == 0:
                    finito = True
                # Dopo aver fatto dei movimenti espando la frontiera
                espandiFrontiera()
            if nroNodiCk % 250000 == 0:
                print("Operazione numero ", nroNodiCk)
        # La mossa porterebbe l'albero ad una proffondità superiore alla massima impostata.
        # Annullo l'ultima azione e rimuovo gli elementi insiriti nella frontiera
        else:
            livello -= 1
            elem = elencoMosse.pop()
            indiceElemento = griglia.index(elem)
            indiceSpazio = griglia.index(0)
            griglia[indiceSpazio] = elem
            griglia[indiceElemento] = 0
            # Elimino dalla frontiera tutti i numeri fino ad arrivare allo 0
            while frontiera[-1] != 0:
                frontiera.pop()
            frontiera.pop()  # Elimino anche lo 0 dalla frontiera
        '''
        print("\n\n")
        stampa(griglia)
        print("Frontiera: ", frontiera, " | Livello: ", livello)
        '''
    elapsed_time = time.time() - start_time

    if finito:
        print("Soluzione trovata in ", elapsed_time, " secondi")
        print("Mosse da eseguire: ", elencoMosse)
        print("Tempo impiegato: ", elapsed_time)
    else:
        print("Soluzione non trovata, nodi esplorati: ", nroNodiCk)
        print("Tempo impiegato: ", elapsed_time)
    ris = str(maxProf) + " " + str(nroNodiCk) + " " + str(elapsed_time) + "\n"
    file.write(ris)
file.close()
