# Problém čínského listonoše
#
# Zadání:
# Listonoš musí zajít na poštu, vzít dopisy a obejít s nimi všechny ulice města a
# nakonec se vrátit do výchozího bodu.
# Musí přitom urazit minimální vzdálenost.


# Algoritmus pro nalezení nejkratší cesty ve váženém grafu, 
# a to za podmínek průchodu # všech hran a návrat do výchozího bodu O.

# Krok 1 : Zjištění jestli je graf Eulerovský, pokud ano jeho uzavřený tah je jeho optimální cesta.
# Krok 2 : Najdeme všechny vrcholy s lichým stupněm.
# Krok 3 : Vytvoříme všechny možné páry lichých vrcholů.
# Krok 4 : Pro každou skupinu párů určíme nejkratší cestu.
# Krok 5 : Najdeme skupinu párů s nejkratší cestou.
# Krok 6 : Upravím graf a to tak že přidáme další hrany z kroku 5
# Krok 7 : Délka nektrtší cesty je součet cest vrchol2 modifikovaném grafu
# Krok 8 : Uzavřený eulerovský tah upraveného grafu je hledaná cesta.

# Příklad:
#                   3
#        (B)----------------(C)
#     1 / |                  | \2
#      /  |                  |  \
#     (A) | 5              6 |  (F)
#      \  |                  |  /
#     2 \ |         4        | /1
#        (D)----------------(E)
#
# Liché vrcholy A, B, C, E
# Možné páry:   B-C,D-E
#               B-D,C-E
#               B-E,C-D
#
# Nalezení nejkratších cest pro páry
#               B-C -> (B-C) 3, D-E -> (D-E) 4 součet = 7
#               B-D -> (B-A A-D) 3, C-E -> (C-F F-E) 3 součet = 6
#               B-E -> (B-C C-F F-E) 6, C-D -> (C-B B-A A-D) 6 součet = 12
#
#               Nejkratší cesta: B-D -> (B-A A-D) 3, C-E -> (C-F F-E) 3 součet = 6
#
# Úprava grafu: Zdvojíme hrany nejkratších cest: (B-A, A-D, C-F, F-E)
#
# Nejkratší celková cesta: je poté součet všech hran vrchol2 neupraveném grafu nebo
# součet nejkratší cesty (B-D) a součet hran vrchol2 neupraveněm grafu
# součet hran vrchol2 upraveném grafu = 24 + 6 = 30
# 
# Trasa je poté uzavřený eulerovský tah: A-B B-C C-E E-F F-C C-F F-E E-D D-A A-D D-B B-A
#
# Zdroje:
# https://www.geeksforgeeks.org/chinese-postman-route-inspection-set-1-introduction/
# https://www.geeksforgeeks.org/fleurys-algorithm-for-printing-eulerian-nejkratsi_cesta/?ref=lbp
# https://towardsdatascience.com/chinese-postman-in-python-8b1187a3e5a
# https://cs.wikipedia.org/wiki/Probl%C3%A9m_%C4%8D%C3%ADnsk%C3%A9ho_listono%C5%A1e


import sys
import queue  # pouzijeme priority queue
from collections import defaultdict

NEKONECNO = sys.maxsize
BEZ_HRANY = 0

class Vertex:
    def __init__(self, vrchol_id):
        self.id = vrchol_id
        self.vzdalenost = 0
        self.predchozi_vrchol = None

class Graph:
    def __init__(self, max_vertices):

        # matice sousednosti pro reprezentaci vzdáleností
        self.matice_sousednosti = [[BEZ_HRANY] * max_vertices for _ in range(max_vertices)] 
        # pomocný spojový seznam pro upravený graf a nelezení cesty 
        self.seznam = defaultdict(list)
        # list uzlu, kazdy uzel ma sve id, pod kterym je najdeme vrchol2 listu uzlu
        self.vrcholy = []
        # aktualni pocet uzlu
        self.velikost_matice = 0  

    # přidání vrcholu
    def pridej_vrchol(self, vrchol_id):
        if self.velikost_matice < len(self.matice_sousednosti):
            self.vrcholy.append(Vertex(vrchol_id))
            self.velikost_matice += 1
    
    def vrchol_existuje(self, vrchol_id):
        return vrchol_id >= 0 and vrchol_id < self.velikost_matice

    # vrátí vrcholy vrchol2 listu
    def vypis_vrcholu(self):
        return [vrchol2.id for vrchol2 in self.vrcholy]

    def sousedni_vrchol(self, vrchol_id):
        vedlejsi_vrchol = []
        if self.vrchol_existuje(vrchol_id):
            for j in range(0, self.velikost_matice):
                if self.matice_sousednosti[vrchol_id][j] != BEZ_HRANY:
                    vedlejsi_vrchol.append(j)
        return vedlejsi_vrchol

    #přidání hrany
    def pridej_hranu(self, pocatecni_vrchol, koncovy_vrchol, vzdalenost):
        if self.vrchol_existuje(pocatecni_vrchol) and self.vrchol_existuje(koncovy_vrchol):
            self.matice_sousednosti[pocatecni_vrchol][koncovy_vrchol] = vzdalenost
            self.matice_sousednosti[koncovy_vrchol][pocatecni_vrchol] = vzdalenost

            self.seznam[pocatecni_vrchol].append(koncovy_vrchol)
            self.seznam[koncovy_vrchol].append(pocatecni_vrchol)

        else:
            raise Exception("Nemůžu vytvořit hranu")

    #přidání pomocných hran pro upravení grafu na Eulerovský graf 
    def pridej_pomocnou_hranu(self, pocatecni_vrchol, koncovy_vrchol):
        if self.vrchol_existuje(pocatecni_vrchol) and self.vrchol_existuje(koncovy_vrchol):
            self.seznam[pocatecni_vrchol].append(koncovy_vrchol)
            self.seznam[koncovy_vrchol].append(pocatecni_vrchol)
        else:
            raise Exception("Nemůžu vytvořit hranu")

    def vrat_hranu(self, pocatecni_vrchol, koncovy_vrchol):
        if self.vrchol_existuje(pocatecni_vrchol) and self.vrchol_existuje(koncovy_vrchol):
            return self.matice_sousednosti[pocatecni_vrchol][koncovy_vrchol]

    # vypíše matici sousednosti grafu
    def vypis_matice_sousednosti(self):
        print("\nAdjecency matice_sousednosti:")
        # pokud budeme mit vrchol2 matici None typ, tak bude vyhazovat err
        # pomoci vnoreneho cyklu
        for sublist in self.matice_sousednosti:
            for i in sublist:
                if i == None:
                    print("{:4}".format(-1), end="", sep="")
                else:
                    print("{:4}".format(i), end="", sep="")
            print("")
        print("")

    # ---------------------------------
    def dijkstra(self, start_vrchol, koncovy_vrchol):
        for vrchol2 in self.vrcholy:
            vrchol2.vzdalenost = NEKONECNO
            vrchol2.predchozi_vrchol = None

        self.vrcholy[start_vrchol].vzdalenost = 0
        OPEN = queue.PriorityQueue()

        for vrchol2 in self.vrcholy:
            OPEN.put((vrchol2.vzdalenost, vrchol2.id))

        while not OPEN.empty():
            current_node_id = OPEN.get()[1] 
            current_node = self.vrcholy[current_node_id]
            for vid in self.sousedni_vrchol(current_node_id):
                edge_distace = self.vrat_hranu(current_node_id, vid)
                vzdalenost = current_node.vzdalenost + edge_distace
                if vzdalenost < self.vrcholy[vid].vzdalenost:
                    self.vrcholy[vid].vzdalenost = vzdalenost
                    self.vrcholy[vid].predchozi_vrchol = current_node
        # backtrack
        nejkratsi_cesta = []
        node = self.vrcholy[koncovy_vrchol]

        while node != None:
            nejkratsi_cesta.append(node.id)
            node = node.predchozi_vrchol

        nejkratsi_cesta.reverse()
        return nejkratsi_cesta

    #-----------------------------------
    # Fleuryho Algoritmus pro nalezení uzavřeného tahu

    #odstraní hranu již jsme prošli
    def odstran_hranu(self, vrchol1, vrchol2):
        for index, key in enumerate(self.seznam[vrchol1]):
            if key == vrchol2:
                self.seznam[vrchol1].pop(index)
        for index, key in enumerate(self.seznam[vrchol2]):
            if key == vrchol1:
                self.seznam[vrchol2].pop(index)

    def prohledavani_do_hloubky(self, vrchol2, prohledano):
        pocitadlo = 1
        prohledano[vrchol2] = True
        for i in self.seznam[vrchol2]:
            if prohledano[i] == False:
                pocitadlo = pocitadlo + self.prohledavani_do_hloubky(i, prohledano)         
        return pocitadlo
 
    # určí zda lze hnou projít
    def dosazitelna_hrana(self, vrchol1, vrchol2):
        if len(self.seznam[vrchol1]) == 1:
            return True
        else: 
            prohledano =[False]*(self.velikost_matice)
            pocitadlo1 = self.prohledavani_do_hloubky(vrchol1, prohledano)
            self.odstran_hranu(vrchol1, vrchol2)
            prohledano =[False]*(self.velikost_matice)
            pocitadlo2 = self.prohledavani_do_hloubky(vrchol1, prohledano)
 
            self.pridej_pomocnou_hranu(vrchol1,vrchol2) 

            return False if pocitadlo1 > pocitadlo2 else True
 
    # Vypiš Eulerovský uzavřený tah který začíná z určitého vrcholu
    def Euleruv_tah_z_vrcholu(self, vrchol_start):
        predposledni_vrchol = 0
        for vrchol2 in self.seznam[vrchol_start]:         
            if self.dosazitelna_hrana(vrchol_start, vrchol2):
                print("%d-%d " %(vrchol_start,vrchol2)),
                self.odstran_hranu(vrchol_start, vrchol2)
                self.Euleruv_tah_z_vrcholu(vrchol2)
                predposledni_vrchol = vrchol2
        return predposledni_vrchol

    # Vypiš Eulerovský uzavřený tah
    def vypis_Eulerova_cyklu(self):
        vrchol1 = 0
        predposledni_vrchol = self.Euleruv_tah_z_vrcholu(vrchol1)
        print("%d-%d " %(predposledni_vrchol,vrchol1)),
        
# Sečte všechny hrany grafu
def SoucetDelkyHran(MaticeSousednosti):
    soucet = 0
    for i in range(len(MaticeSousednosti)):
        for j in range(i,len(MaticeSousednosti)):
            soucet += MaticeSousednosti[i][j]
    return soucet
            
# Dijktrův algorytmus pro hledání nejkratší cesty
def dijktra(graph, start_vrchol, koncovy_vrchol):
    shortest = [0 for i in range(len(graph))]
    selected = [start_vrchol]
    l = len(graph)
   
    min_sel = NEKONECNO
    for i in range(l):
        if(i==start_vrchol):
            shortest[start_vrchol] = 0
        else:
            if(graph[start_vrchol][i]==0):
                shortest[i] = NEKONECNO
            else:
                shortest[i] = graph[start_vrchol][i]
                if(shortest[i] < min_sel):
                    min_sel = shortest[i]
                    ind = i
                
    if(start_vrchol==koncovy_vrchol):
        return 0
    selected.append(ind) 
    while(ind!=koncovy_vrchol):
        for i in range(l):
            if i not in selected:
                if(graph[ind][i]!=0):
                    if((graph[ind][i] + min_sel) < shortest[i]):
                        shortest[i] = graph[ind][i] + min_sel
        temp_min = sys.maxsize 
        for j in range(l):
            if j not in selected:
                if(shortest[j] < temp_min):
                    temp_min = shortest[j]
                    ind = j
        min_sel = temp_min
        selected.append(ind)  
    return shortest[koncovy_vrchol]
                            
# Najdi vlcholy s lichými stupni
def NajdiLicheVrcholy(MaticeSousednosti):
    stupen = [0 for i in range(len(MaticeSousednosti))]
    for i in range(len(MaticeSousednosti)):
        for j in range(len(MaticeSousednosti)):
                if(MaticeSousednosti[i][j]!=0):
                    stupen[i]+=1
    LicheStupne = [i for i in range(len(stupen)) if stupen[i]%2!=0]
    return LicheStupne

# Funkce pro generování párování vrchol2 grafu
def Kombinace_lichych_vrcholu(licheVrcholy):
    Pary = []
    for i in range(len(licheVrcholy)-1):
        Pary.append([])
        for j in range(i+1,len(licheVrcholy)):
            Pary[i].append([licheVrcholy[i],licheVrcholy[j]])
    return Pary

# Najde nejoprimálnější cestu a její vzdálenost a vypíše ji 
def nejoptimalnejsi_cesta(MaticeSousednosti):
    LicheVrcholy = NajdiLicheVrcholy(MaticeSousednosti)
    if(len(LicheVrcholy)==0):
        return SoucetDelkyHran(MaticeSousednosti)
    Pary = Kombinace_lichych_vrcholu(LicheVrcholy)
    l = (len(Pary)+1)//2    
    Seznam_paru = []
    
    def Parovani(Pary, done = [], final = []):
        if(Pary[0][0][0] not in done):
            done.append(Pary[0][0][0])           
            for i in Pary[0]:
                f = final[:]
                val = done[:]
                if(i[1] not in val):
                    f.append(i)
                else:
                    continue
                
                if(len(f)==l):
                    Seznam_paru.append(f)
                    return 
                else:
                    val.append(i[1])
                    Parovani(Pary[1:],val, f)                   
        else:
            Parovani(Pary[1:], done, final)
            
    Parovani(Pary)
    minimalni_hodnota = []
    
    for i in Seznam_paru:
        s = 0
        for j in range(len(i)):
            s += dijktra(MaticeSousednosti, i[j][0], i[j][1])
        minimalni_hodnota.append(s)
    
    minimalni_hodnota_absolutní = min(minimalni_hodnota)
    cesty = []
    position = minimalni_hodnota.index(min(minimalni_hodnota))
    Rozsizene = Seznam_paru[position]
    for j in range(len(Rozsizene)):
        cesty = g.dijkstra(Rozsizene[j][0],Rozsizene[j][1])
        for k in range(len(cesty)-1):
            g.pridej_pomocnou_hranu(cesty[k],cesty[k+1])

    for l in range(len(g.seznam)):
         g.seznam[l].sort()

    print("Nejoptimálnější cesta:")
    g.vypis_Eulerova_cyklu()
    print()
    
    minimálni_delka_cesty = minimalni_hodnota_absolutní + SoucetDelkyHran(MaticeSousednosti)
    print("nejmenší vzdálenost je:" ,minimálni_delka_cesty)    
    
###
# Graph
#                   3
#        (1)----------------(2)
#     1 / |                  | \2
#      /  |                  |  \
#     (0) | 5              6 |  (5)
#      \  |                  |  /
#     2 \ |         4        | /1
#        (3)----------------(4)
#

g = Graph(6)
# přidáme potřebný počet vrcholů
g.pridej_vrchol(0)
g.pridej_vrchol(1)
g.pridej_vrchol(2)
g.pridej_vrchol(3)
g.pridej_vrchol(4)
g.pridej_vrchol(5)

print("Vertices", g.vypis_vrcholu())
print()
# přidáme hrany
g.pridej_hranu(0, 1, 1)
g.pridej_hranu(0, 3, 2)
g.pridej_hranu(1, 2, 3)
g.pridej_hranu(1, 3, 5)
g.pridej_hranu(2, 4, 6)
g.pridej_hranu(2, 5, 2)
g.pridej_hranu(3, 4, 4)
g.pridej_hranu(4, 5, 1)

# vytiskneme si  matici sousednosti
g.vypis_matice_sousednosti()

nejoptimalnejsi_cesta(g.matice_sousednosti)