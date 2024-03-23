# Software is provided "As if" I shall not be held responsible for any data loss

from data import *
from copy import deepcopy
path_to_data = "./Data/"

# Configuration

FiltreInsanite = True
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
Variant = 0
# Français
NombreDeCollesFr = 3
# Entrez un seul nombre pour utiliser un unique variant ou une liste avec le variant pour chaque colle
VariantFr = 10
# Fin de la configuration -----------------------------------

# Données complémentaires - Auto-générées -----------------------------------
Impaires = [Paires[i] for i in range(len(Paires)-1, -1, -1)]
Echec = 0

# Vérification des saisies -----------------------------------

# Variant français
try:
    VariantFr = int(VariantFr)
    VariantFr = [VariantFr for i in range(NombreDeCollesFr)]
except ValueError:
    if len(VariantFr) != NombreDeCollesFr:  # type: ignore
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

# Fonction génératrice


def générateur(Semaine, Coloscope, Trinomes, Matiere, GroupeDeTD):
    '''
    Génère la semaine du coloscope
    '''
    ColoscopeInitial = deepcopy(Coloscope)
    for ListeTrinome in Trinomes:

        for TrinomesAColler in ListeTrinome:

            
            for Colle in Coloscope:
                if Colle['Matiere'] == Matiere:
                    trinome = TrinomesAColler[0]
                    GroupeDeTP = getGroupeTP(trinome, GroupeTP)
                    if dispoEDT(GroupeDeTD+1, GroupeDeTP, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True and dispoEDT(GroupeDeTD+1, GroupeDeTP, Colle['Jour'], demiHeureAprès(Colle['Heure']), str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True:
                        Colle[str(Semaine)] = trinome
                        TrinomesAColler.remove(trinome)
                    else :
                        # print(TrinomesAColler)
                        Coloscope = deepcopy(ColoscopeInitial)
                        # print('Trinome',trinome,'Jour',Colle['Jour'],'heure',Colle['Heure'],dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(
                        #     Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues))
                        break
                if TrinomesAColler == []:
                    return Coloscope
    print('Il semble qu\'il est impossible de générer les colles de cette matière')
    return ColoscopeInitial


Semaines = keepIntAsStr(list(Coloscope[0].keys()))

# Colles de français -----------------------------------

ElevesAColler = []
for Decalage in VariantFr:  # type: ignore
    ElevesAColler += rotate(ListeEleves(Trinomes), Decalage)

# Etude la faisabilité

NbCréneau = 0
FaisabilitéFr = None

for Colle in Coloscope:
    if Colle['Matiere'] == 'Francais':
        NbCréneau += 1
NbCréneau *= len(Semaines)

if NbCréneau < len(ElevesAColler):
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

                    if dispoEleve(GroupeDeTD, GroupeDeTP, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues, rang) == True:
                        Colle[str(Semaine)] = Eleve
                        ElevesAColler.remove(Eleve)
                        ColleAttribuee = True
                        break
                if ElevesAColler == [] or Iteration == MaxIteration:
                    ColleAttribuee = True

if FaisabilitéFr is False:
    print(ElevesAColler)


# Autres colles -----------------------------------


# Combinaison
CombinaisonsGroupeTD = []
for GroupeDeTD in range(len(GroupeTD)):
    CombinaisonsGroupeTD.append(Permutations(GroupeTD[GroupeDeTD]))
# Variant
for GroupeDeTD in range(len(CombinaisonsGroupeTD)):
    CombinaisonsGroupeTD[GroupeDeTD] = rotate(
        CombinaisonsGroupeTD[GroupeDeTD], Variant)

# Generation par semaine du coloscope
Semaines = Semaines


for Semaine in Semaines:
    print('Le programme traite la semaine', Semaine)
    if estPaire(Semaine):
        Combinaison = Paires
    else:
        Combinaison = Impaires
    for GroupeDeTD in range(len(CombinaisonsGroupeTD)):
        for Matiere in Combinaison[GroupeDeTD]:
            print('GroupeDeTD', GroupeDeTD+1, 'Matière', Matiere)
            if Matiere == 'Langues':
                continue

            else:
                Trinomes = deepcopy(CombinaisonsGroupeTD[GroupeDeTD])
                Coloscope = générateur(
                    Semaine, Coloscope, Trinomes, Matiere, GroupeDeTD)
                export_csv('Colloscope', Coloscope)

    for GroupeDeTD in range(len(CombinaisonsGroupeTD)):
        CombinaisonsGroupeTD[GroupeDeTD] = rotate(
            CombinaisonsGroupeTD[GroupeDeTD], 1)
    for langue in ListeLangues:
        GroupeLV1[langue] = rotate(GroupeLV1[langue])
    export_csv('Colloscope', Coloscope)

# Vacances -----------------------------------
for i in Coloscope:
    for j in ['0', '1', '2', '3', '4', '5']:  # Plus de vacances ? Rajoutez-en
        Vacances = 'Vacances'+j
        if Vacances in i.keys():
            i[Vacances] = 'Vacances'

# Export des données -----------------------------------
export_csv('Colloscope', Coloscope)


