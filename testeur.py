from TesteurBackend import *

path_to_data = "./Data/"

# Configuration
Nom='test'
FiltreInsanite = True
ListeLangues = ['Anglais', 'Espagnol', 'Allemand', 'Italien']

# Rotation - Les mêmes que le planning des rotations
Rotation = [{'Nom': 'SI', 'Jour': 'Lundi', 'Heure': '10h00 - 12h30'},
            {'Nom': 'SI', 'Jour': 'Mercredi', 'Heure': '13h30 - 16h00'},
            {'Nom': 'SI', 'Jour': 'Jeudi', 'Heure': '16h30 - 19h00'},
            {'Nom': 'Physique', 'Jour': 'Mercredi', 'Heure': '13h30 - 16h30'},
            {'Nom': 'Info', 'Jour': 'Lundi', 'Heure': '10h00 - 12h00'},
            {'Nom': 'Info', 'Jour': 'Lundi', 'Heure': '17h00 - 19h00'}]


# Import des donnees -----------------------------------
Eleves = import_csv('Groupes')
Trinomes = trinomes(Eleves)
# Liste des groupes de TD / TP par trinome
GroupeTD, GroupeTP = Groupes(Trinomes, 2, 3)
GroupeLV2 = LV2(Trinomes, ListeLangues)
GroupeLV1 = LV1(Trinomes, ListeLangues)
# Emploi du temps
EmploiDuTemps = import_csv('EmploiDuTemps')
# Rotations
Planning = import_csv('Rotation')

# import
Coloscope=import_csv(Nom)

# Vérification --------------------------------

Semaines = keepIntAsStr(list(Coloscope[0].keys()))
enzo = 0

for Semaine in Semaines:
    for Colle in Coloscope:
        trinome = Colle[Semaine]

        if trinome != '':
            Heure = Colle['Heure']
            Jour = Colle['Jour']

            GroupeDeTD = getGroupeTD(trinome,GroupeTD)
            GroupeDeTP = getGroupeTP(trinome,GroupeTP)

            Dispo = dispoEDT(GroupeDeTD, GroupeDeTP, Jour, Heure, str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) 
            DispoDemiHeureAprès = dispoEDT(GroupeDeTD, GroupeDeTP, Jour, demiHeureAprès(Heure), str(
                Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues)
            
            print(trinome,Dispo,DispoDemiHeureAprès)
            if [Dispo,DispoDemiHeureAprès] !=[True,True] :

                Colle[Semaine] = Colle[Semaine] + ' indisponible'
                
                if trinome == '11' :
                    enzo +=1
print(enzo)
export_csv('Coloscope',Coloscope)

        