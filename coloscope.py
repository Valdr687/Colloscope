# Software is provided "As if" I shall not be held responsible for any data loss

from data import *
from copy import deepcopy
path_to_data = "./Data/"

# Configuration

FiltreInsanite=False
Langues = ['Anglais', 'Espagnol', 'Allemand', 'Italien']
Paires = [['Maths', 'Langues'], ['SII', 'Physique-Chimie']]
# En semaine paire le groupe A a les colles de la première paire et le groupe B celles de la deuxième
Impaires = [['SII', 'Physique-Chimie'], ['Maths', 'Langues']]  # Transposee

Rotation = [{'Nom': 'SI', 'Jour': 'Lundi', 'Heure': '10h00 - 12h30'},
            {'Nom': 'SI', 'Jour': 'Mercredi', 'Heure': '13h30 - 16h00'},
            {'Nom': 'SI', 'Jour': 'Jeudi', 'Heure': '16h30 - 19h00'},
            {'Nom': 'Physique', 'Jour': 'Mercredi', 'Heure': '13h30 - 16h30'},
            {'Nom': 'Info', 'Jour': 'Lundi', 'Heure': '10h00 - 12h00'},
            {'Nom': 'Info', 'Jour': 'Lundi', 'Heure': '17h00 - 19h00'}]
Variant=3

# Import des donnees
Eleves = import_csv('Groupes')
Coloscope = import_csv('Coloscope')
Trinomes = trinomes(Eleves)
Colleurs=colleurs(FiltreInsanite,Coloscope)
# Liste des groupes de TD / TP par trinome
GroupeTD, GroupeTP = Groupes(Trinomes, 2, 3)
GroupeLV2 = LV2(Trinomes, Langues)
GroupeLV1 = LV1(Trinomes, Langues)
# Emploi du temps
EmploiDuTemps = import_csv('EmploiDuTemps')
# Rotation
Planning = import_csv('Rotation')

# Generation du coloscope

Semaines = keepIntAsStr(list(Coloscope[0].keys()))
GroupeTD = [rotate(GroupeTD[0], Variant), rotate(GroupeTD[1], Variant)]

#Generation par semaine du coloscope
for Semaine in Semaines:
    if estPaire(Semaine):
        Combinaison=Paires
    else :
        Combinaison=Impaires
    for GroupeDeTD in range(len(GroupeTD)):
        for Matiere in Combinaison[GroupeDeTD]:
            if Matiere == 'Langues':
                continue
                # for Langue in Langues:
                    # Trinomes = deepcopy(GroupeLV1[Langue])
                    # MaxIteration = len(Trinomes)+1
                    # Iteration = 0
                    # if Langue == 'Espagnol':
                    #     print(MaxIteration)
                    # ColleAttribuee = False
                    # while not ColleAttribuee:
                    #     Iteration += 1
                    #     TrinomesEnCours = deepcopy(Trinomes)
                    #     for Colle in Coloscope:
                    #         # Bonne matière
                    #         if Colle['Matiere'] == Langue:
                    #             for trinome in TrinomesEnCours:
                    #                 try :
                    #                     test=int(trinome[-1])
                    #                     GroupeDeTP = getGroupeTP(trinome, GroupeTP)
                    #                     if dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, Langues) == True:
                    #                         Colle[str(Semaine)] = trinome
                    #                         TrinomesEnCours.remove(trinome)
                    #                         break
                    #                 except :
                    #                     print('hi')
                    #                     lettre=trinome[-1]
                    #                     trinome=trinome[:len(trinome)-2]
                    #                     GroupeDeTP = getGroupeTP(trinome, GroupeTP)
                    #                     if dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, Langues) == True:
                    #                         Colle[str(Semaine)] = trinome+lettre
                    #                         TrinomesEnCours.remove(
                    #                             trinome+lettre)
                    #                         break
                                        
                    #     if TrinomesEnCours == [] or Iteration == MaxIteration:
                    #         ColleAttribuee = True
                    #     Trinomes = rotate(Trinomes)
            else:
                Trinomes = deepcopy(GroupeTD[GroupeDeTD])
                MaxIteration = len(Trinomes)+1
                Iteration = 0
                #print("Semaine :", Semaine, "Groupe de TD :", GroupeDeTD+1,"Matiere :", Matiere, "Trinomes :", Trinomes)
                
                ColleAttribuee=False
                while not ColleAttribuee :
                    Iteration+=1
                    TrinomesEnCours = deepcopy(Trinomes)
                    for Colle in Coloscope:
                        #Bonne matière
                        if Colle['Matiere'] == Matiere:
                            #print("Matiere :", Matiere,'Jour',Colle['Jour'],'à',Colle['Heure'])
                            for trinome in TrinomesEnCours:
                                GroupeDeTP = getGroupeTP(trinome,GroupeTP)
                                # print('Semaine', Semaine, 'Jour', Colle['Jour'], 'Heure', Colle['Heure'], 'trinome',trinome,' est ', dispoEDT(
                                #     GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, Langues))
                                if dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, Langues)==True:
                                    Colle[str(Semaine)] = trinome
                                    TrinomesEnCours.remove(trinome)
                                    #print('Colle attribuee à', trinome, ' : trinomes restants', TrinomesEnCours)
                                    break
                    if TrinomesEnCours==[] or Iteration==MaxIteration:
                        ColleAttribuee=True
                    Trinomes=rotate(Trinomes)                    

    for GroupeDeTD in range(len(GroupeTD)): 
        GroupeTD[GroupeDeTD] = rotate(GroupeTD[GroupeDeTD])
    for langue in Langues:
        GroupeLV1[langue]=rotate(GroupeLV1[langue])

for i in Coloscope:
    # Vacances - Parce que
    for j in ['0', '1', '2', '3', '4', '5']:  # Plus de vacances ? Rajoutez-en
        Vacances = 'Vacances'+j
        if Vacances in i.keys():
            i[Vacances] = 'Vacances'

export_csv('Coloscope',Coloscope)



print(GroupeLV1)