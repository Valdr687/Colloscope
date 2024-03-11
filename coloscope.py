# Software is provided "As if" I shall not be held responsible for any data loss

from data import *
from copy import deepcopy
path_to_data = "./Data/"

# Configuration

FiltreInsanite = False
ListeLangues = ['Anglais', 'Espagnol', 'Allemand', 'Italien']
# En semaine paire le groupe A a les colles de la première paire et le groupe B celles de la deuxième
Paires = [['Maths', 'Langues'], ['SII', 'Physique-Chimie']]
# Rotation - Les mêmes que le planning des rotations
Rotation = [{'Nom': 'SI', 'Jour': 'Lundi', 'Heure': '10h00 - 12h30'},
            {'Nom': 'SI', 'Jour': 'Mercredi', 'Heure': '13h30 - 16h00'},
            {'Nom': 'SI', 'Jour': 'Jeudi', 'Heure': '16h30 - 19h00'},
            {'Nom': 'Physique', 'Jour': 'Mercredi', 'Heure': '13h30 - 16h30'},
            {'Nom': 'Info', 'Jour': 'Lundi', 'Heure': '10h00 - 12h00'},
            {'Nom': 'Info', 'Jour': 'Lundi', 'Heure': '17h00 - 19h00'}]
# Variant
Variant = 3
# Français
NombreDeCollesFr = 3
# Entrez un seul nombre pour utiliser un unique variant ou une liste avec le variant pour chaque colle
VariantFr = 10


# Fin de la configuration -----------------------------------

# Données complémentaires - Auto-générées -----------------------------------
Impaires = [Paires[i] for i in range(len(Paires)-1, -1, -1)]

# Vérification des saisies -----------------------------------

# Variant français
try:
    VariantFr = int(VariantFr)
    VariantFr = [VariantFr for i in range(NombreDeCollesFr)]
except ValueError:
    if len(VariantFr) != NombreDeCollesFr:
        print('Une erreur a été détectée : Il manque des variants pour une ou plusieurs colles de français. ', end="")
        VariantFr = [VariantFr[0] for i in range(NombreDeCollesFr)]
        print('Le programme utilisera', VariantFr)

# Import des donnees -----------------------------------
Eleves = import_csv('Groupes')
Coloscope = import_csv('Coloscope')
Trinomes = trinomes(Eleves)
Colleurs = colleurs(FiltreInsanite, Coloscope)
# Liste des groupes de TD / TP par trinome
GroupeTD, GroupeTP = Groupes(Trinomes, 2, 3)
GroupeLV2 = LV2(Trinomes, ListeLangues)
GroupeLV1 = LV1(Trinomes, ListeLangues)
# Emploi du temps
EmploiDuTemps = import_csv('EmploiDuTemps')
# Rotations
Planning = import_csv('Rotation')

# Generation du coloscope

Semaines = keepIntAsStr(list(Coloscope[0].keys()))

# Colles de français -----------------------------------

ElevesAColler = []
for Decalage in VariantFr:
    ElevesAColler += rotate(ListeEleves(Trinomes), Decalage)

# Etude la faisabilité

NbCréneau=0
FaisabilitéFr=None

for Colle in Coloscope :
    if Colle['Matiere'] == 'Francais':
        NbCréneau+=1
NbCréneau*=len(Semaines)

if NbCréneau<len(ElevesAColler):
    print("Il n'a pas assez de créneaux en français, le programme affichera les colles qui n'ont pas été attribuées.")
    FaisabilitéFr = False
    
for Semaine in Semaines:
    for Colle in Coloscope:
        if Colle['Matiere'] == 'Francais':
            MaxIteration = len(ElevesAColler) + 1
            Iteration = 0

            ColleAttribuee = False
            while ColleAttribuee is False:
                Iteration += 1
                for Eleve in ElevesAColler:
                    trinome = Eleve[:len(Eleve)-1]
                    rang = Eleve[-1]

                    GroupeDeTP = getGroupeTP(trinome, GroupeTP)
                    GroupeDeTD = getGroupeTD(trinome, GroupeTD)

                    #print('Semaine', Semaine, 'Jour', Colle['Jour'], 'Heure', Colle['Heure'], 'eleve',Eleve,' est ', dispoEleve(GroupeDeTP, GroupeDeTD, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues,rang))
                    if dispoEleve(GroupeDeTP, GroupeDeTD, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues, rang) == True:
                        Colle[str(Semaine)] = Eleve
                        ElevesAColler.remove(Eleve)
                        ColleAttribuee = True
                        break
                if ElevesAColler == [] or Iteration == MaxIteration:
                    ColleAttribuee = True

if FaisabilitéFr is False :
    print(ElevesAColler)


# Autres colles -----------------------------------

# Variant
for GroupeDeTD in range(len(GroupeTD)):
    GroupeTD[GroupeDeTD] = rotate(GroupeTD[GroupeDeTD], Variant)

# Generation par semaine du coloscope
for Semaine in Semaines:
    if estPaire(Semaine):
        Combinaison = Paires
    else:
        Combinaison = Impaires
    for GroupeDeTD in range(len(GroupeTD)):
        for Matiere in Combinaison[GroupeDeTD]:
            if Matiere == 'Langues':

                for Langue in ListeLangues:

                    Trinomes = []
                    # Enlèvement des élèves de l'autre groupe
                    for trinome in GroupeLV1[Langue]:
                        if ContainLetter(trinome):
                            if getGroupeTD(trinome[:len(trinome)-1], GroupeTD) == str(GroupeDeTD+1):
                                Trinomes.append(trinome)
                        else :
                            if getGroupeTD(trinome,GroupeTD)==str(GroupeDeTD+1):
                                Trinomes.append(trinome)

                    # Enlèvement des élèves isolés de la langue principale ----
                    Liste = []
                    if Langue == ListeLangues[0]:
                        for trinome in Trinomes:
                            
                            if ContainLetter(trinome) :
                                if not trinome[:len(trinome)-1] in Liste:
                                    Liste.append(
                                        trinome[:len(trinome)-1])
                            else:
                                Liste.append(trinome)
                        Trinomes = Liste
                    # ----
                    MaxIteration = len(Trinomes)+1
                    Iteration = 0

                    ColleAttribuee = False
                    while ColleAttribuee is False:
                        Iteration += 1
                        TrinomesEnCours = deepcopy(Trinomes)
                        for Colle in Coloscope:
                            # Bonne matière
                            if Colle['Matiere'] == Langue:
                                    
                                    for trinome in TrinomesEnCours:
                                        GroupeDeTP = getGroupeTP(trinome, GroupeTP)
                                        if dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True:
                                            Colle[str(Semaine)] = trinome
                                            TrinomesEnCours.remove(trinome)
                                            break

                        if TrinomesEnCours == [] or Iteration == MaxIteration:
                            ColleAttribuee = True
                        Trinomes = rotate(Trinomes)
            else:
                Trinomes = deepcopy(GroupeTD[GroupeDeTD])
                MaxIteration = len(Trinomes)+1
                Iteration = 0

                ColleAttribuee = False
                while ColleAttribuee is False:
                    Iteration += 1
                    TrinomesEnCours = deepcopy(Trinomes)
                    for Colle in Coloscope:
                        # Bonne matière
                        if Colle['Matiere'] == Matiere:

                            for trinome in TrinomesEnCours:
                                GroupeDeTP = getGroupeTP(trinome, GroupeTP)
                                if dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True and dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], demiHeureAprès(Colle['Heure']), str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True:
                                    Colle[str(Semaine)] = trinome
                                    TrinomesEnCours.remove(trinome)
                                    break
                    if TrinomesEnCours == [] or Iteration == MaxIteration:
                        ColleAttribuee = True
                    Trinomes = rotate(Trinomes)

    for GroupeDeTD in range(len(GroupeTD)):
        GroupeTD[GroupeDeTD] = rotate(GroupeTD[GroupeDeTD])
    for langue in ListeLangues:
        GroupeLV1[langue] = rotate(GroupeLV1[langue])

# Vacances -----------------------------------
for i in Coloscope:
    for j in ['0', '1', '2', '3', '4', '5']:  # Plus de vacances ? Rajoutez-en
        Vacances = 'Vacances'+j
        if Vacances in i.keys():
            i[Vacances] = 'Vacances'

# Export des données -----------------------------------
export_csv('Coloscope', Coloscope)

