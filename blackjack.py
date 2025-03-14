import random
import time

if input(f"abilita le funzioni di debug?\n'dev' per abilitare le funzioni developer\n[INVIO] per giocare normalmente\n > > ") == "dev":
    dev = True
else:
    dev = False

mazzo = []

        def componi_mazzo():
    global mazzo
    def crea_mazzo():
        global mazzo
        i = (input("Quanti mazzi vuoi usare?\n >> "))
        if i == "" or int(i) <= 0:
            i = 2
            print("Mazzi di default: 2")
        else:
            i = int(i)
        mazzo = []
        while i != 0:
            for x in range(1, 14):
                mazzo.append(f'c{x}')
                mazzo.append(f'q{x}')
                mazzo.append(f'f{x}')
                mazzo.append(f'p{x}')
                random.shuffle(mazzo)
            i -= 1
        if dev == True:
            print(mazzo)
    if dev == True:
        if input("Vuoi comporre il mazzo manualmente?\n[INVIO] per comporre il mazzo automaticamente\n'dev' per comporre il mazzo manualmente\n >> ") == "dev":
            print("MAZZO DI SVILUPPO")
            i = int(input("Inserisci il numero di carte\n >> "))
            while i != 0:
                mazzo.append(input("Inserisci manualemente la carta\n >> "))
                i -= 1
            print(mazzo)
        else:
            crea_mazzo()
    else:
        crea_mazzo()        
    
def devskiptimezawarudo():
    global dev
    if dev == False:
        time.sleep(0.200)

def prendicarta():
    global mazzo
    carta_pescata = mazzo[0]
    mazzo.pop(0)
    return carta_pescata

def pesca_giocatore(carte):
    global carte_giocatore
    carte.append(prendicarta())
    print(f'La mano del giocatore è {carte}')
    for i, x in enumerate(carte):
        valore_carta = int(x[1:])
        if valore_carta == 1:
            carte.append(carte.pop(i))

def controllo_split(*carte_mano):
    global dev
    if dev == True:
        print(carte_mano)
    global splittable
    global carte_giocatore
    splittable = []
    def ciclo_interno(*carte):
        for x in carte:
            semivar1 = 0
            semivar2 = 0
            for y in x:
                if semivar1 == 0:
                    semivar1 = int(y[1]) + len(y)*100
                else:
                    semivar2 = int(y[1]) + len(y)*100
            if semivar1 == semivar2:
                splittable.append(True)
                
            else:
                splittable.append(False)
            if dev == True:
                print(splittable)
                
        if dev == True:
            print(semivar1, semivar2)
        
        

    if carte_giocatore[0] == "multideck":
        for x in carte_giocatore[1:]:
            ciclo_interno(x)
    else:
        ciclo_interno(carte_mano[0])

def pesca_dealer():
    global carte_dealer
    global dealer_time
    if dealer_time == 0:
        carte_dealer.append(prendicarta())
        dealer_time += 1
    elif dealer_time == 1:
        print(f'le carte del dealer sono {carte_dealer} e una carta coperta')
        carte_dealer.append(prendicarta())
        dealer_time += 1
    else:
        carte_dealer.append(prendicarta())
        print(f'le carte del dealer sono {carte_dealer}')
        for i, x in enumerate(carte_dealer):
            valore_carta = int(x[1:])
            if valore_carta == 1:
                carte_dealer.append(carte_dealer.pop(i))

def calcolopunti(carte):
    global gioco
    global punteggio_giocatore
    punti = 0
    for carta in carte:
        if len(carta) == 3:
            punti += 10
        else:
            if int(carta[1]) != 1:
                punti += int(carta[1])
            else:
                if punti > 10:
                    punti += 1
                else:
                    punti += 11
    print(punti)
    return punti

def calcolo_BJ(*carte):
    punti = 0
    for x in carte:
        for y in x:
            if len(y) == 3:
                punti += 10
            else:
                if int(y[1]) != 1:
                    punti += int(y[1])
                else:
                    if punti > 10:
                        punti += 1
                    else:
                        punti += 11
    if punti == 21:
        return "BJ"

def split_giocatore():
    i = 0
    if fiches - puntata[0] < 0:
        print("Impossibile splittare: fiches possedute inferiori alla puntata")
    else:
        for giocate in carte_giocatore:
            if i == len(splittable):
                break 
            elif splittable[i] == True:
                if input("Vuoi splittare?\nINVIO = NO\ns o qualsiasi altro carattere = SI\n >> ") != "":
                    print("SPLIT!")
                    if carte_giocatore[0] == "multideck":
                        pass
                    else: 
                        carte_giocatore.insert(0, "multideck")

                    carte_giocatore.append([giocate[0],prendicarta()])
                    carte_giocatore.append([giocate[1],prendicarta()])
                    carte_giocatore.pop(i+1)
                    if dev == True:
                        print(f"CONTROLLO POST SPLIT{carte_giocatore}")
                    print(f"Le tue carte sono: {carte_giocatore}")
                    controllo_split(carte_giocatore)
                else:
                    print(f"CONTROLLO POST NON SPLIT{carte_giocatore}")
                    i += 1
            else:
                i += 1

def gioco_giocatore():
    global fiches
    global dev
    global puntata
    global punteggio_giocatore
    punteggio_giocatore = []
    i = 0
    k = 0
    if carte_giocatore[0] == "multideck":
        i +=1
    for giocate in carte_giocatore[i:]:
        if calcolo_BJ(giocate) == "BJ":
            punteggio_giocatore.append("BJ")
            i += 1
            k += 1
        else:  
            j = True
            while j:
                    if controllo_raddoppio(puntata) == True:
                        if input("Vuoi readdoppiare?\nINVIO = RADDOPPIO\nn o qualsiasi altro carattere = NON RADDOPPIO\n >> ") == "":
                            fiches = fiches - puntata[k]
                            puntata[k] = puntata[k] * 2
                            pesca_giocatore(giocate)
                            if calcolopunti(giocate) == 21:
                                punteggio_giocatore.append(21)
                            elif calcolopunti(giocate) > 21:
                                print("Sballato")
                                punteggio_giocatore.append(0)
                            else:
                                punti = calcolopunti(giocate)  
                                punteggio_giocatore.append(punti)
                                print(f"Punteggio aggiornato: {punti}")
                            j = False
                        else:
                            if input("Vuoi un'altra carta?\nINVIO = CARTA\nn o qualsiasi altro carattere = STAI\n >> ") == "":
                                pesca_giocatore(giocate)
                                print(calcolopunti(giocate))
                                print(giocate)
                                if calcolopunti(giocate) < 22:
                                    if calcolopunti(giocate) == 21:
                                        punteggio_giocatore.append(21)
                                        j = False
                                    else:
                                        pass
                                else:
                                    print("Sballato")
                                    punteggio_giocatore.append(0)
                                    j = False
                            else:
                                j = False
                                punti = calcolopunti(giocate)  
                                punteggio_giocatore.append(punti)
                                print(f"Punteggio aggiornato: {punti}")  
            k += 1                  

def confronta_punteggio(giocatore, dealer):
    global fiches
    global puntata
    ctrl = 0
    for punteggio in giocatore: 
        if punteggio == "BJ":
            print(f"Vince il giocatore con BLACKJACK contro {dealer}")
            fiches = fiches + (puntata[ctrl] + puntata[ctrl] * 3/2)
        elif punteggio > dealer:
            print(f"Vince il giocatore con {punteggio} contro {dealer}")
            fiches = fiches + (puntata[ctrl] * 2)
        elif punteggio == dealer:
            print(f"Pareggio! Entrambi con {punteggio}")
            fiches = fiches + puntata[ctrl]
        else:
            print(f"Vince il dealer con {dealer} contro {punteggio}")
            puntata[ctrl] = 0
        ctrl +=1 

def gioco_dealer():
    global punteggio_dealer
    global punteggio_giocatore
    global carte_dealer
    global dev
    i = 0
    while i == 0:
        devskiptimezawarudo()
        punti = 0
        for x in carte_dealer:
            if len(x) == 3:
                punti += 10
            else:
                if int(x[1]) != 1:
                    punti += int(x[1])
                else:
                    if punti > 10:
                        punti += 1
                    else:
                        punti += 11
            if dev == True:
                print(carte_dealer)
            punteggio_dealer = punti
            if dev == True:
                print(f"CONTROLLO PUNTI {punteggio_dealer}")

        print(f"Il punteggio del dealer è {punteggio_dealer}")

        if punteggio_dealer == 21 and len(carte_dealer) != 2:
            punteggio_dealer = 21
            i = 1
        elif punteggio_dealer > 21:
            punteggio_dealer = 0
            i = 1
        elif punteggio_dealer < 17:
            if dev == True:
                print("CONTROLLO RIPESCATA DEALER")
            for x in punteggio_giocatore:
                x += x
            if x == 0:
                i = 1
            else:
                controllerBJ = 0
                for x in punteggio_giocatore:
                    if x == "BJ":
                        controllerBJ += 1
                        print("CONTROLLO ALL BJ 1")
                if controllerBJ == len(splittable):
                    i = 1
                    print("CONTROLLO ALL BJ 2")
                else:    
                    pesca_dealer()
                    if dev == True:
                        print("CONTROLLO 1")
        else:
            if dev == True:
                print("CONTROLLO CHIUSURA RIPESCATA DEALER")
            i = 1
    if dev == True:
        print("CONTROLLO 2")
    
    confronta_punteggio(punteggio_giocatore, punteggio_dealer)

def getlistpuntata(puntata):
    global dev
    puntata = [puntata]    
    if dev == True:
        print(puntata)
    return puntata

def controllo_raddoppio(puntata):
    global fiches
    if fiches - puntata[0] < 0:
        return False
    else:
        return True

def puntate_multiple():
    global puntata
    global splittable
    global dev
    global fiches
    print(f"CONTROLLO PUNTATA {puntata}")
    for x in splittable[1:]:
        puntata.append(puntata[0])
        fiches = fiches - puntata[0]
        if dev == True:
            print(puntata)

mainLoop = True

componi_mazzo()
fiches = 1000

print("Il giocatore inizia con 1000 fiches\nLe puntate devono essere multipli di 10")

while mainLoop == True: 
    
    print(f"Il giocatore ha {fiches} fiches")
    print(f"Il mazzo è composto da {len(mazzo)} carte\n")
    (input("Carte > > [invio]\n >> "))

    carte_giocatore = []
    carte_dealer = []
    punteggio_giocatore = 0
    punteggio_dealer = 0
    dealer_time = -1
    splittable = []
    gioco = True
    
    while dealer_time == -1:
        puntata = input("Inserire la puntata [INVIO] (min 10) >> ")
        if puntata == "":
            puntata = 10
            fiches = fiches - puntata
            dealer_time = 0
            print("Inserita la puntata minima di 10 fiches")
        else:
            puntata = int(puntata)
            if puntata/10 - int(puntata/10) != 0:
                print("Puntata non valida")       
            else:
                if puntata > fiches:
                    print("Puntata maggiore delle fiches possedute")
                else:
                    fiches = fiches - puntata
                    dealer_time = 0

    pesca_giocatore(carte_giocatore)
    devskiptimezawarudo()
    pesca_dealer()
    devskiptimezawarudo()
    pesca_giocatore(carte_giocatore)
    devskiptimezawarudo()
    pesca_dealer()
    devskiptimezawarudo()

    if calcolo_BJ(carte_dealer) == "BJ" and calcolo_BJ(carte_giocatore) == "BJ":
        print("PUSH!")
        print(f"le carte del dealer sono {carte_dealer}")
        print(f"le carte del giocatore sono {carte_giocatore}")
        fiches = fiches + puntata
    elif calcolo_BJ(carte_dealer) == "BJ":
        print("Il dealer ha un Blackjack!")
        print(f"le carte del dealer sono {carte_dealer}")
        print(f"le carte del giocatore sono {carte_giocatore}")
        print("Il dealer vince! con blackjack")
        puntata = 0 
    elif calcolo_BJ(carte_giocatore) == "BJ":
        print("Il giocatore ha un Blackjack!")
        print(f"le carte del dealer sono {carte_dealer}")
        print(f"le carte del giocatore sono {carte_giocatore}")
        print("Il giocatore vince! con blackjack")
        fiches = fiches + (puntata + puntata * 3/2)  
    else:
        puntata = getlistpuntata(puntata)
        calcolopunti(carte_giocatore)
        controllo_split(carte_giocatore)
        while gioco == True:
            carte_giocatore = [carte_giocatore]
            if dev == True:
                print(carte_giocatore)
            split_giocatore()
            puntate_multiple()
            gioco_giocatore()
            gioco = False

        print(f"Il tuo punteggio finale è > {punteggio_giocatore}")
        print("turno del dealer")
 
        gioco_dealer()

    if (input("Vuoi iniziare una nuova partita?\n[INVIO] = SI\nn o qualsiasi altro carattere = ESCI\n >> ")) != "":
        break
    else:
        print("Inizio partita")
        if len(mazzo) < 20:
            print("Il mazzo è finito, mescolo le carte")
            componi_mazzo()
