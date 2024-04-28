# Bibliothèques
from cryptography.fernet import Fernet
from itertools import permutations 
import csv
import pandas as pd
from tkinter import messagebox
# Variables
path_to_data = "./Data/"
alphabet = {'A': 1, 'B': 2, 'C': 3}
Langues = []  # Langues possibles
Trinomes = []
Coloscope = None
EmploiDuTemps = None
Colleurs = None
Planning = None
Rotation = None

# Import des données


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


def import_csv(fichier, path=path_to_data):
    lecteur = csv.DictReader(open(path+fichier + '.csv', 'r'))
    return [dict(ligne) for ligne in lecteur] # type: ignore


def export_csv(nom, file):
    df = pd.DataFrame(file)
    df.to_csv(nom+'.csv', index=False)


def trinomes(Eleves):
    Liste = []
    SousListe = []
    rang = 1
    for i in range(len(Eleves)):
        if rang == int(Eleves[i]['trinome']):
            SousListe.append(Eleves[i])

        else:
            Liste.append(SousListe)
            rang = int(Eleves[i]['trinome'])
            SousListe = [Eleves[i]]
    Liste.append(SousListe)
    return Liste


def ListeEleves(Trinomes):
    Liste = []
    for trinome in Trinomes:
        for eleve in trinome:
            Liste.append(eleve['trinome']+eleve['Rang'])

    return Liste


def Groupes(Trinomes, NombreDemiGroupe, NombreTierGroupe):
    GroupeTD = [[] for i in range(NombreDemiGroupe)]
    GroupeTP = [[] for i in range(NombreTierGroupe)]

    for i in range(len(Trinomes)):
        GroupeTD[alphabet[Trinomes[i][0]['Gr. TD']] -
                 1].append(Trinomes[i][0]['trinome'])
        GroupeTP[int(Trinomes[i][0]['Gr.TP']) -
                 1].append(Trinomes[i][0]['trinome'])

    return (GroupeTD, GroupeTP)

def GroupesColle(Trinomes,NombreGroupe):
    Liste = [[] for i in range(NombreGroupe)]

    for i in range(len(Trinomes)):
        Liste[int(Trinomes[i][0]['Gr. Colle']) - 1].append(Trinomes[i][0]['trinome'])

    return Liste

key = b'heVfpWafIoe0PDpF-K1YP0cL79dp8OEOAkKPoqXXshk='
token = b'gAAAAABl-I16B48WafZbbLYBzrS6_sfdFyZZZsn7tNNOvP4YxJl-gzcUJkUu-HO_3d-Pf6vCuRCGwWcxzbXhSiB-JeYF8YsvVA=='


def LV1(Trinomes, Langues):
    Liste = {Langue: [] for Langue in Langues}
    for trinome in Trinomes:
        for eleve in trinome:
            if eleve['LV1'] in Langues:
                Liste[eleve['LV1']].append(eleve['trinome']+eleve['Rang'])

    for ListeTrinomes in Liste.values():
        if not ListeTrinomes == []:
            # Autant de liste que le numéro de trinome du dernier trinome
            TrinomesEnCours = [[] for j in range(
                int(ListeTrinomes[-1][0:len(ListeTrinomes[-1])-1]))]
            for Eleve in ListeTrinomes:
                EleveEnCours = Eleve[0:len(Eleve)-1]
                TrinomesEnCours[int(EleveEnCours)-1].append(int(EleveEnCours))
            for Trinome in TrinomesEnCours:
                if not Trinome == []:

                    if len(Trinome) >= 3:
                        ListeTrinomes.append(str(Trinome[0])[0:len(Trinome)-1])
                        lettre = ['a', 'b', 'c', 'd', 'e']
                        for k in range(len(Trinome)):
                            try:
                                ListeTrinomes.remove(str(Trinome[k])+lettre[k])
                            except:
                                print(
                                    "Vérifiez vos données - Cause probable : deux lettres se suivent")
    return Liste


def LV2(Trinomes, Langues):
    Liste = {Langue: [] for Langue in Langues}
    for trinome in Trinomes:
        for eleve in trinome:
            if eleve['LV2'] in Langues:
                Liste[eleve['LV2']].append(eleve['trinome']+eleve['Rang'])

    for ListeTrinomes in Liste.values():
        if not ListeTrinomes == []:
            # Autant de liste que le numéro de trinome du dernier trinome
            TrinomesEnCours = [[] for j in range(
                int(ListeTrinomes[-1][0:len(ListeTrinomes[-1])-1]))]
            for Eleve in ListeTrinomes:
                EleveEnCours = Eleve[0:len(Eleve)-1]
                TrinomesEnCours[int(EleveEnCours)-1].append(int(EleveEnCours))
            for Trinome in TrinomesEnCours:
                if not Trinome == []:

                    if len(Trinome) >= 3:
                        ListeTrinomes.append(str(Trinome[0])[0:len(Trinome)-1])
                        lettre = ['a', 'b', 'c', 'd', 'e']
                        for k in range(len(Trinome)):
                            try:
                                ListeTrinomes.remove(str(Trinome[k])+lettre[k])
                            except:
                                print(
                                    "Vérifiez vos données - Cause probable : deux lettres se suivent")
    return Liste


def colleurs(Filtre, Coloscope : list):
    Liste = [{'Nom': Coloscope[0]['Nom'], 'Matiere': Coloscope[0]['Matiere'],
              'Creneaux': [{'Creneau': [Coloscope[0]['Jour'], Coloscope[0]['Heure']], 'Salle': Coloscope[0]['Salle']}]}]
    DernierColleur = 0
    for i in range(len(Coloscope)):

        ColleursEnCours = {'Nom': '', 'Matiere': '',
                           'Creneaux': []}
        ColleursEnCours['Nom'] = Coloscope[i]['Nom']

        secret = decrypt(token, key).decode()
        secret=str(secret)
        if secret in ColleursEnCours['Nom'].lower() and Filtre:
            messagebox.showwarning(
                "Error", "The coloscope you're using appear to contain a forbidden word. The author of this program does not condone child abuse and verbal violence.")
            exit()
        Jour = Coloscope[i]['Jour']
        Heure = Coloscope[i]['Heure']
        Salle = Coloscope[i]['Salle']
        if ColleursEnCours['Nom'] == Liste[DernierColleur]['Nom']:
            Liste[DernierColleur]['Creneaux'].append(
                {'Creneau': [Jour, Heure], 'Salle': Salle})
        else:
            DernierColleur += 1
            ColleursEnCours['Matiere'] = Coloscope[i]['Matiere']
            ColleursEnCours['Creneaux'].append(
                {'Creneau': [Jour, Heure], 'Salle': Salle})
            Liste.append(ColleursEnCours)

    return Liste

# Fonctions traitements


def ContainLetter(string):
    if string == '':
        return False
    try:
        string = int(string)
        return False
    except:
        return True


def keepIntAsStr(List):  # From a list with integers and strings keep integers as strings
    Liste = []
    for i in List:
        try:
            i = int(i)
            Liste.append(str(i))
        except:
            continue
    return Liste


def estPaire(str):
    try:
        str = int(str)
    except:
        print(Exception)
    return str % 2 == 0


def rotate(l, y=1):
    if len(l) == 0:
        return l
    y = y % len(l)

    return l[y:] + l[:y]


def getGroupeTP(trinome, GroupeTP):
    if ContainLetter(trinome):
        trinome = trinome[:-1]
    for i in range(len(GroupeTP)):
        if trinome in GroupeTP[i]:
            return str(i+1)


def getGroupeTD(trinome, GroupeTD):
    if ContainLetter(trinome):
        trinome = trinome[:-1]
    for i in range(len(GroupeTD)):
        if trinome in GroupeTD[i]:
            return str(i+1)
        

def getGroupeColle(trinome, GroupeColle):
    if ContainLetter(trinome):
        trinome = trinome[:-1]
    for i in range(len(GroupeColle)):
        if trinome in GroupeColle[i]:
            return str(i+1)
# Fonction temporelles


def demiHeureAprès(heure):
    heure = str(heure)
    if heure[-1] == 'h':
        return heure+'30'
    elif heure[-2:] == '00':
        return heure[:len(heure)-2]+'30'
    elif heure[-2:] == '30':
        incrément = 0
        try:
            incrément = int(heure[:2])+1
        except:
            incrément = int(heure[1])+1
        return str(incrément)+'h'


def heureAprès(heure):
    heure = str(heure)
    h = 0
    for rang in range(len(heure)):
        if heure[rang] == 'h':
            h = rang
    return str(int(heure[:h])+1)+heure[h:]

# Disponibilités


def dispoRT(GroupeTD, GroupeTP, jour, heure, semaine, Rotations, Planning, trinome, coloscope):
    if heure[-1]=='h' :
        heure += '00'
    for Ligne in Planning:
        if Ligne['Semaine'] == semaine:
            RangRotation = 0
            for rotation in Rotations:
                if rotation['Jour'] == jour and heure >= rotation['Heure'][:5] and heure < rotation['Heure'][-5:]:
                    if Ligne['Rotation'+str(RangRotation)] in ['TD'+str(GroupeTD), 'TP'+str(GroupeTP)]:
                        return 'en tp/td'
                    if Ligne['Rotation'+str(RangRotation)] == 'Cours':
                        return 'en cours - rotation'
                    if Ligne['Rotation'+str(RangRotation)] == 'Libre':
                        return dispoColle(coloscope, trinome, semaine, heure, jour)
                RangRotation += 1
    return dispoColle(coloscope, trinome, semaine, heure, jour)


def dispoLangues(trinome, GroupesLV1, GroupesLV2, Langues):
    trinome = str(trinome)
    for Langue in Langues:
        if Langue != 'Anglais':
            for i in GroupesLV1[Langue]+GroupesLV2[Langue]:
                
                if trinome == i[:len(i)-1] :
                    return 'en LV1 / LV2'
                if trinome == i:
                    return 'en LV1 / LV2'
    return True


def dispoLanguesEleve(trinome, GroupesLV1, GroupesLV2, Langues, rang):
    for Langue in Langues:
        if Langue != 'Anglais':
            for i in GroupesLV1[Langue]+GroupesLV2[Langue]:
                if trinome+rang == i or trinome == i:
                    return 'en LV1 / LV2'
    return True


def dispoColle(coloscope, trinome, semaine, heure, jour):
    for Ligne in coloscope:
        trinomeTest = Ligne[semaine]
        if ContainLetter(trinomeTest):
            trinomeTest = trinomeTest[:len(trinomeTest)-1]
        if trinomeTest == trinome:
            if Ligne['Jour'] == jour:
                if Ligne['Heure'][-2:] == '30':
                    if Ligne['Heure'][:2] == heure[:2] or str(int(Ligne['Heure'][:2])+1) == heure[:2]:
                        return 'en colle'
                if Ligne['Heure'][:2] == heure[:2]:
                    return 'en colle'
    return True


def dispoEDT(GroupeTD, GroupeTP, jour, heure, semaine, Rotation, Planning, EDT, trinome, coloscope, GroupesLV1, GroupesLV2, Langues):
    for i in EDT:
        if i['Jour'] == jour:
            if i[heure] in ['Libre', 'Alternance']:
                return dispoColle(coloscope, trinome, semaine, heure, jour)
            if i[heure] == 'Cours':
                return 'en cours'
            if i[heure] == 'Langues':
                return dispoLangues(trinome, GroupesLV1, GroupesLV2, Langues)
            if i[heure] == 'Rotation':
                
                return dispoRT(GroupeTD, GroupeTP, jour, heure, semaine, Rotation, Planning, trinome, coloscope)
            if i[heure] == 'Pause':
                return dispoEDT(GroupeTD, GroupeTP, jour, heureAprès(heure), semaine, Rotation, Planning, EDT, trinome, coloscope, GroupesLV1, GroupesLV2, Langues)
    return False


def dispoEleve(GroupeTD, GroupeTP, jour, heure, semaine, Rotation, Planning, EDT, trinome, coloscope, GroupesLV1, GroupesLV2, Langues,rang) :
    troncage = False
    if heure[-2:] == '00':
        heure = heure[:len(heure)-2]
        troncage = True
    for i in EDT:
        if i['Jour'] == jour:
            if i[heure] in ['Libre', 'Alternance']:
                return dispoColle(coloscope, trinome, semaine, heure, jour)
            if i[heure] == 'Cours':
                return 'en cours'
            if i[heure] == 'Langues':
                return dispoLanguesEleve(trinome, GroupesLV1, GroupesLV2, Langues, rang)
            if i[heure] == 'Rotation':
                
                if troncage:
                    return dispoRT(GroupeTD, GroupeTP, jour, heure+'00', semaine, Rotation, Planning, trinome, coloscope)
                else:
                    return dispoRT(GroupeTD, GroupeTP, jour, heure, semaine, Rotation, Planning, trinome, coloscope)
            if i[heure] == 'Pause':
                return dispoEDT(GroupeTD, GroupeTP, jour, heureAprès(heure), semaine, Rotation, Planning, EDT, trinome, coloscope, GroupesLV1, GroupesLV2, Langues)
    return 'False par défaut'

def Permutations(Liste):
    Permutations = list(permutations(Liste))
    listeCombinaison=[]
    SousListe = []
    if Liste==[]:
        return Permutations
    if len(Liste)==1:
        return [[[Permutations[0][0]]]]
    PremierTrinome = Permutations[0][0]
    for i in Permutations :
        if i[0]==PremierTrinome:
            SousListe.append(list(i))
        else :
            PremierTrinome = i[0]
            listeCombinaison.append(SousListe)
            SousListe = [list(i)]
    listeCombinaison.append(SousListe)
           
    return listeCombinaison

