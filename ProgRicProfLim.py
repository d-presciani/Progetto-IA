# TODO: Leggere
# https://heuristicswiki.wikispaces.com/N+-+Puzzle

from random import shuffle


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


# Funzione per controllo correttezza griglia
def controlla():
    grigliaCorr = list(range(1, 16))
    grigliaCorr.append(0)
    if griglia == grigliaCorr:
        return True
    else:
        return False


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
        # Inserire controllo cicli


# Calcolo della distanza di Manhattan per la griglia data
def manhattanDistance():
    md = 0
    for elem in griglia:
        if elem != 0:
            deltaY = abs((elem-1) // 4 - griglia.index(elem) // 4)
            deltaX = abs((elem-1) % 4 - griglia.index(elem) % 4)
            md += deltaX + deltaY
    return md


# Funzione per espansione della frontiera
def espandiFrontiera():
    frontiera.append(0)  # Lo 0 viene utilizzato per segnare i livelli
    indice = griglia.index(0)
    posX = indice % 4
    posY = indice // 4
    if posX == 0:
        if(ckInserimento(griglia[indice+1])):
            frontiera.append(griglia[indice+1])
    elif posX > 0 and posX < 3:
        if(ckInserimento(griglia[indice+1])):
            frontiera.append(griglia[indice+1])
        if(ckInserimento(griglia[indice-1])):
            frontiera.append(griglia[indice-1])
    elif posX == 3:
        if(ckInserimento(griglia[indice-1])):
            frontiera.append(griglia[indice-1])
    if posY == 0:
        if(ckInserimento(griglia[indice+4])):
            frontiera.append(griglia[indice+4])
    elif posY > 0 and posY < 3:
        if(ckInserimento(griglia[indice+4])):
            frontiera.append(griglia[indice+4])
        if(ckInserimento(griglia[indice-4])):
            frontiera.append(griglia[indice-4])
    elif posY == 3:
        if(ckInserimento(griglia[indice-4])):
            frontiera.append(griglia[indice-4])
    global livello
    livello += 1
    return


# Generazione griglia e shuffle
griglia = [i for i in range(16)]
shuffle(griglia)

# Variabili
frontiera = []
elencoMosse = []
livello = 0
maxProf = 16
finito = False
nroNodiCk = 0

# Main
print(griglia, '\n')
stampa()
print("Controllo griglia random: ", controlla())
print()
# Inizialmente inserisco tutti gli elementi limitrofi a 0 nella frontiera
espandiFrontiera()
print("Frontiera: ", frontiera)
print("Distanza di Manhattan: ", manhattanDistance())
# Fino a quando non ho finito gli elementi nella frontiera oppure non ho trovato una soluzione
while len(frontiera) != 0 and not finito and False:
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
            finito = controlla()
            # Dopo aver o fatto dei movimenti espando la frontiera
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
        while frontiera[-1] != 0:
            frontiera.pop()
        frontiera.pop()
    # print("\nReport:\n", stampa(), "\nStato frontiera: ", frontiera, "\nStato mosse:", elencoMosse, "\nLivello: ",
    #      livello, " | Numero nodi: ", nroNodiCk)
print("Fine")
if finito:
    stampa
else:
    print("Soluzione non trovata, nodi esplorati: ", nroNodiCk)
