"""
Cum funcționează:
1. Se stabilește o populație inițială de indivizi (raze aleatorii).
2. Fiecare individ este evaluat prin funcția de fitness (inversul ariei suprafeței).
3. Se realizează selecția indivizilor cu fitness mai ridicat pentru reproducere.
4. Se aplică operații de crossover și mutație pentru a genera o nouă populație.
5. Procesul se repetă pentru un număr determinat de generații.
6. La final, se obține cea mai bună soluție găsită (raza și înălțimea dozei cu aria minimală).

Ciclul de viață al AG:
- Inițializare → Evaluare → Selecție → Crossover → Mutație → Re-evaluare și iterare până la condiția de oprire.

Astfel, acest exemplu ilustrează cum un AG poate fi folosit pentru a rezolva probleme de optimizare geometrică.
"""
import random
import math

# Volum fix al dozei cilindrice (V0)
VOLUM_FIX = 1000.0  # unități cubice

# Limite pentru raza (r)
RAZA_MIN = 0.1   # Raza minimă posibilă
RAZA_MAX = 10.0  # Raza maximă posibilă

# Parametrii Algoritmului Genetic
DIMENSIUNE_POPULATIE = 50   # Numărul de indivizi din populație
NUMAR_GENERATII = 100       # Numărul de generații pentru evoluție
RATA_MUTATIE = 0.1          # Probabilitatea de mutație
RATA_CROSSOVER = 0.8        # Probabilitatea de crossover

def initializare_populatie():
    """
    Creează o populație inițială de indivizi cu valori ale razei generate aleator.
    """
    return [random.uniform(RAZA_MIN, RAZA_MAX) for _ in range(DIMENSIUNE_POPULATIE)]

def calculeaza_inaltimea(raza):
    """
    Calculează înălțimea (h) a cilindrului dată fiind raza (r) și volumul fix (V0).
    """
    return VOLUM_FIX / (math.pi * raza ** 2)

def calculeaza_aria(raza):
    """
    Calculează aria suprafeței (S) a cilindrului dată fiind raza (r).
    """
    inaltime = calculeaza_inaltimea(raza)
    aria_laterala = 2 * math.pi * raza * inaltime   # Aria laterală
    aria_capace = 2 * math.pi * raza ** 2           # Aria capacelor (sus și jos)
    return aria_laterala + aria_capace

def evalueaza_fitness(raza):
    """
    Evaluează fitness-ul unui individ cu o anumită rază (r).
    Fitness-ul este inversul ariei suprafeței, deoarece vrem să minimizăm această arie.
    """
    aria = calculeaza_aria(raza)
    return 1 / aria  # Un fitness mai mare corespunde unei arii a suprafeței mai mici

def efectueaza_selectia(populatie, valori_fitness):
    """
    Efectuează selecția tip roată de ruletă pentru a alege indivizii din generația următoare.
    """
    fitness_total = sum(valori_fitness)
    probabilitati_selectie = [f / fitness_total for f in valori_fitness]
    indivizi_selectati = []
    for _ in range(DIMENSIUNE_POPULATIE):
        alegere = random.random()
        prob_cumulativa = 0.0
        for individ, p in zip(populatie, probabilitati_selectie):
            prob_cumulativa += p
            if alegere <= prob_cumulativa:
                indivizi_selectati.append(individ)
                break
    return indivizi_selectati

def efectueaza_crossover(parinte1, parinte2):
    """
    Efectuează un crossover aritmetic între doi părinți pentru a produce un urmaș.
    """ 
    alfa = random.random()
    raza_copil = alfa * parinte1 + (1 - alfa) * parinte2
    # Asigură-te că raza copilului este în limitele permise
    raza_copil = max(RAZA_MIN, min(RAZA_MAX, raza_copil))
    return raza_copil

def efectueaza_mutatia(raza):
    """
    Mutează raza unui individ folosind o mutație gaussiană.
    """
    deviatie_standard = 0.1  # Deviatia standard pentru mutație
    raza_mutata = raza + random.gauss(0, deviatie_standard)
    # Asigură-te că raza mutată este în limitele permise
    raza_mutata = max(RAZA_MIN, min(RAZA_MAX, raza_mutata))
    return raza_mutata

def algoritm_genetic():
    """
    Funcția principală care rulează algoritmul genetic pentru a găsi dimensiunile optime ale dozei.
    """
    # Inițializează populația
    populatie = initializare_populatie()

    for generatie in range(NUMAR_GENERATII):
        # Evaluează fitness-ul populației curente
        valori_fitness = [evalueaza_fitness(r) for r in populatie]
        fitness_maxim = max(valori_fitness)
        fitness_mediu = sum(valori_fitness) / len(valori_fitness)
        
        # Selecție
        indivizi_selectati = efectueaza_selectia(populatie, valori_fitness)
        
        # Crossover pentru a produce urmași
        urmasi = []
        for i in range(0, DIMENSIUNE_POPULATIE, 2):
            parinte1 = indivizi_selectati[i]
            parinte2 = indivizi_selectati[(i + 1) % DIMENSIUNE_POPULATIE]
            if random.random() < RATA_CROSSOVER:
                copil1 = efectueaza_crossover(parinte1, parinte2)
                copil2 = efectueaza_crossover(parinte2, parinte1)
                urmasi.extend([copil1, copil2])
            else:
                urmasi.extend([parinte1, parinte2])
        
        # Mutație
        numar_mutatii = 0
        for i in range(len(urmasi)):
            if random.random() < RATA_MUTATIE:
                urmasi[i] = efectueaza_mutatia(urmasi[i])
                numar_mutatii += 1
        
        # Actualizează populația cu noua generație
        populatie = urmasi

        # Afișează progresul la fiecare 10 generații, inclusiv numărul de mutații
        if generatie % 10 == 0 or generatie == NUMAR_GENERATII - 1:
            print(f"\nGenerația {generatie}: Fitness Maxim = {fitness_maxim:.6f}, Fitness Mediu = {fitness_mediu:.6f}, Mutații = {numar_mutatii}")
            
    # După finalizare, găsește cel mai bun individ
    valori_fitness = [evalueaza_fitness(r) for r in populatie]
    index_max = valori_fitness.index(max(valori_fitness))
    raza_optima = populatie[index_max]
    inaltime_optima = calculeaza_inaltimea(raza_optima)
    aria_minima = calculeaza_aria(raza_optima)
    
    print("\nSoluția Algoritmului Genetic:")
    print(f"Raza optimă: {raza_optima:.6f} unități")
    print(f"Înălțimea optimă: {inaltime_optima:.6f} unități")
    print(f"Aria minimă a suprafeței: {aria_minima:.6f} unități pătrate")
    
    # Soluția analitică pentru verificare
    raza_optima_analitica = (VOLUM_FIX / (2 * math.pi)) ** (1 / 3)
    inaltime_optima_analitica = 2 * raza_optima_analitica
    aria_minima_analitica = calculeaza_aria(raza_optima_analitica)
    
    print("\nSoluția Analitică:")
    print(f"Raza optimă: {raza_optima_analitica:.6f} unități")
    print(f"Înălțimea optimă: {inaltime_optima_analitica:.6f} unități")
    print(f"Aria minimă a suprafeței: {aria_minima_analitica:.6f} unități pătrate")

# Rulează algoritmul genetic
if __name__ == "__main__":
    algoritm_genetic()
