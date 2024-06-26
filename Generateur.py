# Software is provided "As if" I shall not be held responsible for any data loss

from Backend.Generator import *
from copy import deepcopy
from time import * # type: ignore
path_to_data = "./Data/"
t1 = time()

# Configuration

FiltreInsanite = True
ListeLangues = ['Anglais', 'Espagnol', 'Allemand', 'Italien']
# En semaine paire le groupe 1 a les colles de la première paire et le groupe 2 celles de la deuxième
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
        VariantFr = [VariantFr[0] for i in range(NombreDeCollesFr)] # type: ignore
        print('Le programme utilisera', VariantFr)

# Import des donnees -----------------------------------
Eleves = import_csv('Groupes')
Coloscope = import_csv('Colloscope')
Trinomes = trinomes(Eleves)
Colleurs = colleurs(FiltreInsanite, Coloscope)
# Liste des groupes de TD / TP / Colle par trinome
GroupeTD, GroupeTP = Groupes(Trinomes, 2, 3)
GroupeLV2 = LV2(Trinomes, ListeLangues)
GroupeLV1 = LV1(Trinomes, ListeLangues)
GroupeColle = GroupesColle(Trinomes,2)
# Emploi du temps
EmploiDuTemps = import_csv('EmploiDuTemps')
# Rotations
Planning = import_csv('Rotation')

# Generation du coloscope -----------------------------------

# Fonction génératrice

def générateur(Semaine, Coloscope, Trinomes, Matiere):
    '''
    Génère la semaine du coloscope
    '''
    # Cas particulier
    if Trinomes == [()]:
        print('Pas de trinome à coller')
        return Coloscope
    
    ColoscopeInitial = deepcopy(Coloscope)
    # Vérification préliminaire
    NombreDeColle = 0
    NombreDeTrinome = len(Trinomes[0][0])
    for Colle in Coloscope :
        if Colle['Matiere'] == Matiere:
            NombreDeColle +=1
    
    DegréLiberté = NombreDeColle - NombreDeTrinome
    MargeUtilisée = 0

    if NombreDeTrinome > NombreDeColle :
        print("Il manque des créneaux de colle, vérifiez vos entrées")
        return Coloscope
    
    MeilleureCombinaison = []
    MeilleurRemplissage = len(Trinomes[0])+1
    Globale = -1
    Locale = -1

    TrinomesIntact = deepcopy(Trinomes)
    for ListeTrinome in Trinomes:
        #print(ListeTrinome[0][0])
        Globale += 1
        Locale = -1
        MargeUtilisée = 0

        for TrinomesAColler in ListeTrinome:
            
            Locale += 1
            for Colle in Coloscope:
                if Colle['Matiere'] == Matiere:
                    trinome = TrinomesAColler[0]
                    GroupeDeTP = getGroupeTP(trinome, GroupeTP)
                    GroupeDeTD = getGroupeTD(trinome, GroupeTD)
                    if dispoEDT(GroupeDeTD, GroupeDeTP, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True and dispoEDT(GroupeDeTD, GroupeDeTP, Colle['Jour'], demiHeureAprès(Colle['Heure']), str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True:
                        Colle[str(Semaine)] = trinome
                        TrinomesAColler.remove(trinome)
                    else :
                        if len(TrinomesAColler) < MeilleurRemplissage :
                            MeilleurRemplissage = len(TrinomesAColler)
                            try :
                                MeilleureCombinaison = TrinomesIntact[Globale][Locale]
                            except :
                                print(Locale)
                        Coloscope = deepcopy(ColoscopeInitial)
                        if MargeUtilisée < DegréLiberté :
                            MargeUtilisée +=1
                            #print('Colle suivante')
                        else :
                            break
                            
                if TrinomesAColler == []:
                    return Coloscope
            
        
        #print(MeilleureCombinaison,MeilleurRemplissage)
    Rang = 0
    MeilleurRemplissage = NombreDeTrinome - MeilleurRemplissage
    for Colle in Coloscope :
        if Colle['Matiere'] == Matiere:
            

            if MeilleureCombinaison == []:
                return Coloscope
            
            trinome = MeilleureCombinaison[0]

            if Rang<MeilleurRemplissage:
                Colle[str(Semaine)] = trinome
            else :
                Colle[str(Semaine)] = trinome + ' à déplacer'
            MeilleureCombinaison.remove(trinome)

            Rang += 1
    return Coloscope

Semaines = keepIntAsStr(list(Coloscope[0].keys()))

def test(trinome,heure,jour,semaine):
    TD = getGroupeTD(trinome,GroupeTD)

    TP = getGroupeTP(trinome,GroupeTP)
    Dispo = dispoEDT(TD,TP,jour,heure,semaine,Rotation,Planning,EmploiDuTemps,trinome,Coloscope,GroupeLV1,GroupeLV2,ListeLangues)
    print(trinome,heure,jour,semaine,Dispo)
    Dispo = dispoEDT(TD, TP, jour, demiHeureAprès(heure), semaine, Rotation, Planning,
                     EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues)
    print(trinome, demiHeureAprès(heure), jour, semaine, Dispo)

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

# Colles sauf langues

# Combinaison
CombinaisonsGroupeColle = []
for GroupeDeColle in range(len(GroupeColle)):
    CombinaisonsGroupeColle.append(Permutations(GroupeColle[GroupeDeColle]))
# Variant
for GroupeDeColle in range(len(CombinaisonsGroupeColle)):
    CombinaisonsGroupeColle[GroupeDeColle] = rotate(
        CombinaisonsGroupeColle[GroupeDeColle], Variant)
    
# Colles de langues

# Enlèvement des élèves isolés de la langue principale 
CombinaisonsLangues = {}
for Langue in ListeLangues:
    CombinaisonsLangues[Langue]=[]

    Liste=[]
    if Langue == ListeLangues[0]:
        for trinome in GroupeLV1[Langue]:
            if ContainLetter(trinome):
                if not trinome[:len(trinome)-1] in Liste:
                    Liste.append(trinome[:len(trinome)-1])
            else :
                Liste.append(trinome)
        GroupeLV1[Langue] = Liste
    CombinaisonsLangueEnCours = [[],[]]
    for trinome in GroupeLV1[Langue]:
        GroupeDeColle = int(getGroupeColle(trinome, GroupeColle)) # type: ignore
        CombinaisonsLangueEnCours[GroupeDeColle -1].append(trinome)
    for GroupeDeColle in range(len(CombinaisonsLangueEnCours)):
        CombinaisonsLangues[Langue].append(Permutations(
            CombinaisonsLangueEnCours[GroupeDeColle]))
# Generation par semaine du coloscope


for Semaine in Semaines:
    print('Le programme traite la semaine', Semaine)
    if estPaire(Semaine):
        Combinaison = Paires
    else:
        Combinaison = Impaires
    for GroupeDeColle in range(len(CombinaisonsGroupeColle)):
        for Matiere in Combinaison[GroupeDeColle]:
            print('Groupe de colle', GroupeDeColle+1, 'Matière', Matiere)
            if Matiere == 'Langues':
                for Langue in ListeLangues :
                    print('Groupe de colle', GroupeDeColle+1, 'Matière', Langue)
                    Trinomes = deepcopy(CombinaisonsLangues[Langue][GroupeDeColle])
                    Coloscope = générateur(Semaine, Coloscope, Trinomes, Langue)
                    export_csv('Colloscope', Coloscope)
            else:
                Trinomes = deepcopy(CombinaisonsGroupeColle[GroupeDeColle])
                Coloscope = générateur(
                    Semaine, Coloscope, Trinomes, Matiere)
                export_csv('Colloscope', Coloscope)

    for GroupeDeColle in range(len(CombinaisonsGroupeColle)):
        CombinaisonsGroupeColle[GroupeDeColle] = rotate(
            CombinaisonsGroupeColle[GroupeDeColle], 1)
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

TempsExécution = time()-t1

print("Fin de l’exécution du programme en", convert(TempsExécution))
