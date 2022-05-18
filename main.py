from fonctions import *

inverse = {"r_agent": "r_agent-1","r_agent-1": "r_agent", "r_patient": "r_patient-1", "r_patient": "r_patient-1" ,"r_isa": "r_hypo","r_hypo": "r_isa" ,"r_holo": "r_has_part", "r_has_part": "r_holo","r_lieu": "r_lieu-1", "r_lieu-1": "r_lieu"}
mot = input("Entrez votre entité 1 : ")
rel = input("Entrez votre relation : ")
ent = input("Entrez votre entité 2 : ")



createTxt(mot,True,"")
createJSON(mot,True,"")
data = getData(mot,True,"")
"""##recuperation des entitées"""

infos = getIdEnt(mot,ent,data)
idEnt = infos["idEnt"]
idMot = infos["idMot"]

"""#Recuperer la relation"""

if idEnt != "null":
    idRt = getIdRel(rel,data)

"""##Voir si la relation existe entre les 2 entités"""

#if idRt != -1:
    #resultat = isRelEntrante(idEnt,idRt,data)

"""## Traiter le cas ou la relation n'est pas directe

###Trouver une entié commune
"""
if True:
    createTxt(ent,False,"")
    createJSON(ent,False,"")
    dataEnt = getData(ent,False,"")
    #idCommuns = getIdCommuns(data,dataEnt,idEnt,idMot)
    relationTransitive = ["r_lieu","r_lieu-1","r_isa","r_holo","r_hypo", "r_has_part","r_own","r_own-1","r_product_of","r_similar"]

    print("***********preuve Transitive***********")
    if rel in relationTransitive:
        if transitiviteV2(data,dataEnt,idMot,idEnt,idRt,mot,rel,ent,3) == False:
            print("Pas de preuve")
    else :
        print("La relation n'est pas transitive")

    print("***********preuve Déductive***********")
    if deductionV2(data,dataEnt,idMot,idEnt,idRt,mot,rel,ent,3) == False:
        print("Pas de preuve")
    print("***********preuve Inductive***********")
    if inductionV2(data,dataEnt,idMot,idEnt,idRt,mot,rel,ent,1) == False:
        print("Pas de preuve")


    if rel in inverse:
        print("*********************************************prouver l'inverse*********************************************")
        rel_1 = inverse[rel]
        print("Prouvons : " + ent + " " + rel_1 + " " + mot)

        createTxt(ent, True, "")
        createJSON(ent, True, "")
        dataEnt = getData(ent, True, "")

        idRt_1 = getIdRel(rel_1,dataEnt)

        createTxt(ent, False, "")
        createJSON(ent, False, "")
        data = getData(mot, False, "")
        print("***********preuve Transitive***********")
        if rel_1 in relationTransitive:
            if transitiviteV2(dataEnt, data, idEnt, idMot, idRt_1, ent, rel_1, mot, 3) == False:
                print("Pas de preuve")
        else:
            print("La relation n'est pas transitive")

        print("***********preuve Déductive***********")
        if deductionV2(dataEnt, data, idEnt, idMot, idRt_1, ent, rel_1, mot, 3) == False:
            print("Pas de preuve")
        print("***********preuve Inductive***********")
        if inductionV2(dataEnt, data, idEnt, idMot, idRt_1, ent, rel_1, mot, 1) == False:
            print("Pas de preuve")
