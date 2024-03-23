#     for Langue in ListeLangues:

#         Trinomes = []
#         # Enlèvement des élèves de l'autre groupe
#         for trinome in GroupeLV1[Langue]:
#             if ContainLetter(trinome):
#                 if getGroupeTD(trinome[:len(trinome)-1], GroupeTD) == str(GroupeDeTD+1):
#                     Trinomes.append(trinome)
#             else :
#                 if getGroupeTD(trinome,GroupeTD)==str(GroupeDeTD+1):
#                     Trinomes.append(trinome)

#         # Enlèvement des élèves isolés de la langue principale ----
#         Liste = []
#         if Langue == ListeLangues[0]:
#             for trinome in Trinomes:

#                 if ContainLetter(trinome) :
#                     if not trinome[:len(trinome)-1] in Liste:
#                         Liste.append(
#                             trinome[:len(trinome)-1])
#                 else:
#                     Liste.append(trinome)
#             Trinomes = Liste
#         # ----
#         MaxIteration = len(Trinomes)+1
#         Iteration = 0

#         ColleAttribuee = False
#         while ColleAttribuee is False:
#             Iteration += 1
#             TrinomesEnCours = deepcopy(Trinomes)
#             for Colle in Coloscope:
#                 # Bonne matière
#                 if Colle['Matiere'] == Langue:

#                         for trinome in TrinomesEnCours:
#                             GroupeDeTP = getGroupeTP(trinome, GroupeTP)
#                             if dispoEDT(GroupeDeTP, GroupeDeTD+1, Colle['Jour'], Colle['Heure'], str(Semaine), Rotation, Planning, EmploiDuTemps, trinome, Coloscope, GroupeLV1, GroupeLV2, ListeLangues) == True:
#                                 Colle[str(Semaine)] = trinome
#                                 TrinomesEnCours.remove(trinome)
#                                 break

#                 if ElevesAColler == [] or Iteration == MaxIteration:
#                     ColleAttribuee = True
#             Trinomes = rotate(Trinomes)
#     Echec+=len(TrinomesEnCours)
