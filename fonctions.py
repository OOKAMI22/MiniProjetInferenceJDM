import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
# import sys
import os
# import selenium
# import bs4
from bs4 import BeautifulSoup as bs
# import pandas as pd
import requests
# import urllib.request
import json

"""## Connexion au Drive

"""


def getHtml(mot,entrant,rel):
    with requests.Session() as s:
        url = 'http://www.jeuxdemots.org/rezo-dump.php?'
        if entrant:
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot,'rel' : rel,'relin': 'norelout' }
        else:
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot, 'rel':rel ,'relout': 'norelin'}

        r = s.get(url, params=payload)
        soup = bs(r.text, 'html.parser')
        prod = soup.find_all('code')
        #print("prod : "+str(type(prod)))
        while("MUTED_PLEASE_RESEND" in str(prod)):
            print("ERREUR")
            r = s.get(url, params=payload)
            soup = bs(r.text, 'html.parser')
            prod = soup.find_all('code')

    return prod



def createTxt(mot,entrant,rel):
    prod = getHtml(mot,entrant,rel)
    mot = mot.replace(" ", "_")
    mot = mot.replace("'", "")
    # print(mot)
    if entrant :
        fileTxtName = mot.replace(" ", "_") +rel+ "_e.txt"
    else :
        fileTxtName = mot.replace(" ", "_") +rel+ "_s.txt"

    try:
        filesize = os.path.getsize(fileTxtName)
        # print("Ce fichier existe ")
    except OSError:
        # print("Ce fichier n'existe pas")
        filesize = 0

    if filesize == 0:

        if entrant:
            fileTxtName = mot.replace(" ", "_") + rel+"_e.txt"
        else:
            fileTxtName = mot.replace(" ", "_") + rel+"_s.txt"

        fileTxt = open(fileTxtName, "w", encoding="utf-8")
        fileTxt.write(str(prod))
        fileTxt.close()

    return fileTxtName


"""## **Convertir le txt en JSON **

"""


def mySplit(expression):
    resultat = []
    tmp = ""
    cond = False
    for i in range(len(expression)):
        if i + 1 == len(expression):
            tmp += expression[i]
            resultat.append(tmp)
        else:
            if expression[i] == "\'" and expression[i + 1] != ";":
                cond = True
            elif expression[i] == "\'" and expression[i + 1] == ";":
                cond = False
            if cond == True:
                tmp += expression[i]
            if cond == False and expression[i] != ";":
                tmp += expression[i]
            elif cond == False and expression[i] == ";":
                resultat.append(tmp)
                tmp = ""

    return resultat


def createJSON(mot,entrant,rel):
    mot = mot.replace(" ", "_")
    mot = mot.replace("'", "")
    if entrant:
        fileJSONName = mot +rel+"_e.json"
    else:
        fileJSONName = mot + rel+"_s.json"
    try:
        filesize = os.path.getsize(fileJSONName)
        # print("Ce fichier existe ")
    except OSError:
        # print("Ce fichier n'existe pas")
        filesize = 0

    if True:
        # Ouvrir le fichier txt en lecture
        if entrant :
            fileTxt = open(mot +rel+ "_e.txt", "r", encoding="utf-8")
        else :
            fileTxt = open(mot +rel+ "_s.txt", "r", encoding="utf-8")
        lines = fileTxt.readlines()

        # Ouvrir le fichierJSON en écriture
        fileJSON = open(fileJSONName, "w", encoding="utf-8")

        fields_nt = ['ntname']
        fields_e = ["name", "type", "w", "formated name"]
        fields_rt = ['trname', 'trgpname', 'rthelp']
        fields_r = ["node1", "node2", "type", "w"]

        # fields_type = ["e", "nt", "rt", "r"]

        dict0 = {}
        dict_e = {}
        dict_rt = {}
        dict_r = {}
        dict_nt = {}



        for i in range(len(lines)):
            description = list(mySplit(lines[i].strip()))
            # print(description)
            if (len(description) > 0):
                if description[0] == "nt":
                    dict2 = {}
                    id = description[1]
                    for i in range(1):
                        dict2[fields_nt[i]] = description[i + 2]

                    dict_nt[id] = dict2


                elif description[0] == "e":
                    dict2 = {}
                    id = description[1]
                    for i in range(3):
                        dict2[fields_e[i]] = description[i + 2]

                    if len(description) > 5:
                        dict2[fields_e[3]] = description[5]

                    dict_e[id] = dict2


                elif description[0] == "rt":
                    dict2 = {}
                    id = description[1]
                    for i in range(2):
                        dict2[fields_rt[i]] = description[i + 2]

                    if len(description) > 4:
                        dict2[fields_rt[2]] = description[4]

                    dict_rt[id] = dict2

                elif (description[0] == "r") :
                    dict2 = {}
                    id = description[1]
                    for i in range(4):
                        dict2[fields_r[i]] = description[i + 2]
                    dict_r[id] = dict2



        dict0["nt"] = dict_nt
        dict0["e"] = dict_e
        dict0["r"] = dict_r
        dict0["rt"] = dict_rt
        json.dump(dict0, fileJSON, indent=4)

        fileJSON.close()
        fileTxt.close()
        # print("tout s'est bien passé")
    return fileJSONName


def getData(mot,entrant,rel):
    createTxt(mot,entrant,rel)
    createJSON(mot,entrant,rel)
    mot = mot.replace(" ", "_")
    # Ouvrir le fichier  Json en lecture
    if entrant :
        fileJSONName = mot +rel+ "_e.json"
    else:
        fileJSONName = mot +rel+ "_s.json"
    fileJSON = open(fileJSONName, "r")
    data = json.load(fileJSON)
    fileJSON.close()
    return data


def getIdEnt(mot, ent, data):
    jsonData = data["e"]

    idEnt = -1
    idMot = -1
    # print(jsonData)
    for entity in jsonData:
        name = jsonData[entity]['name']
        x = name.replace("'", "", 2)
        if x == ent:
            print(entity + ": ")
            print(jsonData[entity]['name'])
            idEnt = entity
        if x == mot:
            print(entity + ": ")
            print(jsonData[entity]['name'])
            idMot = entity

    result = {"idEnt": idEnt, "idMot": idMot}
    return result


def getIdRel(rel, data):
    jsonDataRt = data["rt"]
    idRt = -1
    # print(jsonDataRt)
    for entity in jsonDataRt:
        name = jsonDataRt[entity]['trname']
        x = name.replace("'", "", 2)
        if x == rel:
            # print(entity + ": ")
            # print(jsonDataRt[entity]['trname'])
            idRt = entity
            break
    return idRt


def isRelEntrante(idEnt, idRt, data):
    jsonDataR = data["r"]
    resultat = False
    w = ""
    #print(idEnt)
    #print(len(jsonDataR))
    for entity in jsonDataR:
        node2 = jsonDataR[entity]['node1']
        x = node2.replace("'", "", 2)
        type = jsonDataR[entity]['type']
        y = type.replace("'", "", 2)
        #print("x{}:idEnt{}".format(x,idEnt))
        #print("y{}:idRt{}".format(y,idRt))
        w = jsonDataR[entity]["w"]

        if x == idEnt and y == idRt :
            #print(entity + ": ")
            #print(jsonDataR[entity]['node1'])
            resultat = True

            break
    return [resultat,w]



def isRelSortantePositive(idEnt, idRt, data):
    jsonDataR = data["r"]
    resultat = False
    # print(jsonDataR)
    for entity in jsonDataR:
        node2 = jsonDataR[entity]['node2']
        x = node2.replace("'", "", 2)
        type = jsonDataR[entity]['type']
        y = type.replace("'", "", 2)
        #print("x{}:idEnt{}".format(x, idEnt))
        #print("y{}:idRt{}".format(y, idRt))

        if x == idEnt and y == idRt and ("-" not in jsonDataR[entity]["w"]):
            # print(entity + ": ")
            # print(jsonDataR[entity]['node1'])
            resultat = True
            # print("Bingo")
            break
    return resultat


def isRelSortanteNegative(idEnt, idRt, data):
    jsonDataR = data["r"]
    resultat = False
    # print(jsonDataR)
    for entity in jsonDataR:
        node2 = jsonDataR[entity]['node2']
        x = node2.replace("'", "", 2)
        type = jsonDataR[entity]['type']
        y = type.replace("'", "", 2)

        if x == idEnt and y == idRt and ("-" in jsonDataR[entity]["w"]):
            # print(entity + ": ")
            # print(jsonDataR[entity]['node1'])
            resultat = True
            # print("Bingo")
            break
    return resultat




def poids(M):
    return int(M[2])

def getEntTrans(data, idRt, idMot,mot,rel):
    jsonDataE = data["e"]
    jsonDataR = data["r"]
    #len(jsonDataR[idRt])

    resultat = []
    for relation in jsonDataR:
        if (jsonDataR[relation]['type'] == idRt and ("-") not in jsonDataR[relation]['w']  ):
            node2 = jsonDataR[relation]['node2']
            x = node2.replace("'", "", 2)
            if (jsonDataE[x]['type'] == '1' and x != idMot):
                resultat.append([x, jsonDataE[x]['name'],jsonDataR[relation]['w']])
    resultat = sorted(resultat,key=poids,reverse = True)

    if len(resultat) == 0:
        dataRel = getData(mot,True,rel)
        jsonDataE = dataRel["e"]
        jsonDataR = dataRel["r"]
        for relation in jsonDataR:
            if (jsonDataR[relation]['type'] == idRt and ("-") not in jsonDataR[relation]['w']):
                node2 = jsonDataR[relation]['node2']
                x = node2.replace("'", "", 2)
                if (jsonDataE[x]['type'] == '1' and x != idMot):
                    resultat.append([x, jsonDataE[x]['name'], jsonDataR[relation]['w']])
        resultat = sorted(resultat, key=poids, reverse=True)

    return resultat


def getGenerique(data, idMot,mot,rel):
    dico_generalisation = {"r_isa": "6", "r_holo": "10"}
    if rel in dico_generalisation:
        del dico_generalisation[rel]
    resultat = {}
    for key in dico_generalisation:
        # print(key)
        resultat[key] = getEntTrans(data, dico_generalisation[key], idMot,mot,key)
    # print(resultat)

    return resultat


def getSpecifique(data, idMot,mot,rel):
    dico_specialisation = {"r_hypo": "8", "r_has_part": "9"}
    if rel in dico_specialisation:
        del dico_specialisation[rel]
    resultat = {}
    for key in dico_specialisation:
        # print(key)
        resultat[key] = getEntTrans(data, dico_specialisation[key], idMot,mot,key)

    # print(resultat)

    return resultat


def deduction(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt):
    trouve = False
    idCommuns = getGenerique(data, idMot,mot,rel)
    for idCommun in idCommuns:
        for entity in idCommuns[idCommun]:

            if cpt > 0:

                dataCommuns = getData(entity[1].replace("'", ""),False)
                if isRelSortantePositive(idEnt, idRt, dataCommuns):
                    trouve = True
                    # print("***********Bingo***********")
                    print("OUI car : " + mot + " " + idCommun + " " + entity[1].replace("'", ""))
                    print("et " + entity[1].replace("'", "") + " " + rel + " " + ent)
                    cpt -= 1
                if isRelSortanteNegative(idCommun[0], idRt, dataCommuns):
                    print("Non car : " + mot + " " + idCommun + " " + entity[1].replace("'", ""))
                    print("et " + entity[1].replace("'", "") + " " + rel + " " + ent + " est trés peu probable")
                    cpt = cpt - 1


    return trouve


def induction(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt):
    trouve = False

    idCommuns = getSpecifique(data, idMot,mot,rel)
    for idCommun in idCommuns:
        for entity in idCommuns[idCommun]:

            if cpt > 0:

                dataCommuns = getData(entity[1].replace("'", ""),False)
                if isRelSortantePositive(idEnt, idRt, dataCommuns):
                    trouve = True
                    # print("***********Bingo***********")
                    print("OUI car : " + mot + " " + idCommun + " " + entity[1].replace("'", ""))
                    print("et " + entity[1].replace("'", "") + " " + rel + " " + ent)
                    cpt -= 1
                if isRelSortanteNegative(idCommun[0], idRt, dataCommuns):
                    print("Non car : " + mot + " " + idCommun + " " + entity[1].replace("'", ""))
                    print("et " + entity[1].replace("'", "") + " " + rel + " " + ent + "e st trés peu probable")
                    cpt = cpt - 1


    return trouve


# transitivité
def transitivite(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt):
    trouve = False

    idCommuns = getEntTrans(data, idRt, idMot,mot,rel)
    for idCommun in idCommuns:

        if cpt > 0:

            dataCommuns = getData(idCommun[1].replace("'", ""),False)
            if isRelSortantePositive(idEnt, idRt, dataCommuns):
                trouve = True
                # print("***********Bingo***********")
                print("OUI car : " + mot + " " + rel + " " + idCommun[1].replace("'", ""))
                print("et " + idCommun[1].replace("'", "") + " " + rel + " " + ent)
                cpt -= 1
            else:
                if isRelSortanteNegative(idCommun[0], idRt, dataCommuns):
                    trouve = True
                    print("Non car : " + mot + " " + rel + " " + idCommun[1].replace("'", "") )
                    print("et " + idCommun[1].replace("'", "") + " " + rel + " " + ent + " est trés peu probable")
                    cpt = cpt - 1


    return trouve




def transitiviteV2(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt):
    resultat = False
    idCommuns = getEntTrans(data, idRt, idMot,mot,rel)

    for idCommun in idCommuns:

        if cpt > 0:
            teste = isRelEntrante(idCommun[0], idRt, dataEnt)
            isRelE = teste[0]
            if isRelE:
                resultat = True
                if "-" not in teste[1]:
                    print("OUI car : " + mot + " " + rel + " " + idCommun[1].replace("'", "") + " (Poids : "+idCommun[2].replace("'", "")+")")
                    print("et " + idCommun[1].replace("'", "") + " " + rel + " " + ent + "(Poids : "+teste[1].replace("'", "")+")")
                    cpt = cpt - 1
                else:
                    print("Non car : " + mot + " " + rel + " " + idCommun[1].replace("'", "") )
                    print("et " + idCommun[1].replace("'", "") + " " + rel + " " + ent + "est faux" + "(Poids : "+teste[1].replace("'", "")+")")
                    cpt = cpt - 1
    return resultat




def deductionV2(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt):
    trouve = False
    idCommuns = getGenerique(data, idMot,mot,rel)
    for idCommun in idCommuns:
        for entity in idCommuns[idCommun]:

            if cpt > 0:
                teste = isRelEntrante(entity[0], idRt, dataEnt)
                isRelE = teste[0]

                if isRelE:
                    trouve = True
                    if "-" not in teste[1]:
                        print("OUI car : " + mot + " " + idCommun + " " + entity[1].replace("'", "")+" (Poinds : "+entity[2].replace("'", "")+")")
                        print("et " + entity[1].replace("'", "") + " " + rel + " " + ent + "(Poids : "+teste[1].replace("'", "")+")")
                        cpt -= 1
                    else:
                        print("Non car : " + mot + " " + idCommun + " " + entity[1].replace("'", ""))
                        print("et " + entity[1].replace("'", "") + " " + rel + " " + ent + " est faux" + "(Poids : "+teste[1].replace("'", "")+")")
                        cpt = cpt - 1


    return trouve


def inductionV2(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt):
    trouve = False
    negative = 0
    idCommuns = getSpecifique(data, idMot,mot,rel)
    for idCommun in idCommuns:
        for entity in idCommuns[idCommun]:

            if cpt > 0:
                teste = isRelEntrante(entity[0], idRt, dataEnt)
                isRelE = teste[0]
                if isRelE:
                    trouve = True
                    if "-" not in teste[1]:

                        print("OUI car : " + mot + " " + idCommun + " " + entity[1].replace("'", "")+" (Poinds : "+entity[2].replace("'", "")+")")
                        print("et " + entity[1].replace("'", "") + " " + rel + " " + ent + "(Poids : "+teste[1].replace("'", "")+")")
                        cpt -= 1
                    else:
                        negative += 1
                        if(negative == len(idCommuns)):
                         print("Non car : " + mot + " " + idCommun + " " + entity[1].replace("'", ""))
                         print("et " + entity[1].replace("'", "") + " " + rel + " " + ent + " est faux")
                         cpt = cpt - 1


    return trouve