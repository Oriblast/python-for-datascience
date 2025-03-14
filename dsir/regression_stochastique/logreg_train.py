from describe import *
import numpy as np
import pandas as pd 
import os 
import math
import csv
import sys
s1 = "set"


def make_data2(b, value, house):
    house += "_biais.csv" 
    with open(house, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows([b, value])

def make_data1(arow1, arow2, set_):
    with open(set_ + "_featureW.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(arow1)
        writer.writerow(arow2)

def maj_b(b2, feature, y2, set_name, i):
    """il s'agit de la dérivé du cout j sur le biais b"""

    if (feature["set"][i] == set_name):
        y = 1
    else:
        y = 0
    b1 = y2 - y
    b = b2.iloc[0, 0] - b2.iloc[0, 1] * b1
    make_data2(["b", "a"], [b, 0.03], set_name)

def maj_w(w2, feature, y2, set_name, a, i):
    w = w2.copy()
    """il s'agit de la dérivé du cout j sur le poid w  """
    for j in feature.columns:
        if j != "set":
            if (feature["set"][i] == set_name):
                y = 1
            else:
                y = 0
            w.loc[0, j] = (y2 - y) * feature[j][i]

    for j in w2.columns:
        w2.loc[0, j] = w2.loc[0, j] - a * w[j][0]
    make_data1(columnsName_ls(w2), columns_ls(w2), set_name)

def sigmoïde(feature, w, b, set_name, b2):
    """sigmoide fonction to determine probability y"""
    z = [0.0] * len(feature)
    y2 = [0] * len(feature)
    for i in feature.columns:
        if i != s1:
            for j in range(len(feature)):
                z[j] = feature[i][j] * w[i][0] + b
                y2[j] = 1 / (1 + math.exp(-z[j]))
                maj_b(b2, feature, y2[j], set_name, j)
                maj_w(w, feature, y2[j], set_name, b2["a"][0], j)
    return y2

def columnsName_ls(feature):
    clist = [""] * len(feature.columns)  # Pré-allocation
    j = 0
    for i in feature.columns:
        clist[j] = i
        j += 1
    return clist

def columns_ls(feature):
    ls =  [0.0] * (len(feature.columns))
    for col in feature.columns:
        for i in range(len(feature.columns)):
            ls[i] = feature[col][0]
    return ls

def log_loss(feature, set_name, y2):
    """y2 est la list des prédictions"""
    ll = 0
    for i in range(len(feature)):
        if (feature["set"][i] == set_name):
            y = 1
        else:
            y = 0
        if (y2[i] == 0 or y2[i] == 0.0):
            ll += y * math.log(1e-10) + (1 - y) * math.log(1 - 1e-10)
        else:
            ll += y * math.log(y2[i]) + (1 - y) * math.log(1 - y2[i])
    
    ll = -(1/ len(feature)) * ll
    print(set_name)
    print(ll)
    return ll



def rLogistic_train(feature, set_name):
    """entrainement donné """
    if not os.path.exists(set_name + "_biais.csv") or not os.path.exists(set_name + "_featureW.csv"):
        make_data2(["b", "a"], [0, 0.03], set_name)
        ls = columnsName_ls(feature)
        ls.pop(0)
        init_data = [0.0] * len(ls)
        make_data1(ls, init_data, set_name)
    data_b = pd.read_csv(set_name + "_biais.csv")
    data_w = pd.read_csv(set_name + "_featureW.csv")
    y2 = sigmoïde(feature, data_w, data_b.iloc[0, 0], set_name, data_b)
    j = log_loss(feature, set_name, y2)
    if j > 0.01:
        return j
    else:
        return 1
    return 0

def check_nan(data):
    feature = pd.DataFrame(data)
    for i in feature.columns:
        if i != s1:
            moyenne = feature[i].mean()
            #check_nb_str(feature[i])
            for j in range(len(feature)):
                if np.isnan(feature[i][j]):
                    feature.loc[j, i] = moyenne
            #feature[i].fillna(moyenne)

    return feature

def main ():
    """initialisation"""
    if not os.path.exists("dataset_train.csv"):
        print("fichier d'entrainement inexistant. File : dataset_train.csv")
        return
    data = pd.read_csv("dataset_train.csv")

    for i in data.columns:
        if i == "Astronomy" or i == "Care of Magical Creatures" or i == "Ancient Runes" or i == "Herbology" or i == "Muggle Studies" or i == "Divination" or i == "Flying" or i == "Charms" or i == "Defense Against the Dark Arts" or i == "Transfiguration" or i == "Potions":
        #if i != "Hogwarts House":
            #check_nb_str(data[i])
            for j in range(len(data)):
                data.loc[j, i] /= 100000
    feat1 = {
        "set" : data["Hogwarts House"],
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Muggle Studies" : data["Muggle Studies"]
       # "Ancient Runes" : data["Ancient Runes"]
    }
    feat2 = {
        "set" : data["Hogwarts House"],
        #"Astronomy": data["Astronomy"],
        #"Herbology": data["Herbology"],
        #"Defense Against the Dark Arts": data["Defense Against the Dark Arts"],
        "Divination" : data["Divination"],
        #"Potions" : data["Potions"],
        
        #"Care of Magical Creatures" : data["Care of Magical Creatures"],
        
        #"Muggle Studies" : data["Muggle Studies"]
        #"Ancient Runes" : data["Ancient Runes"]
        "Charms" : data["Charms"],
        "Flying" : data["Flying"]
        #"Transfiguration" : data["Transfiguration"]
    }
    feat3 = {
        "set" : data["Hogwarts House"],
        #"Astronomy": data["Astronomy"],
        #"Herbology": data["Herbology"],
        "History of Magic" : data["History of Magic"],
        "Flying" : data["Flying"]
        #"Ancient Runes" : data["Ancient Runes"]
        #"Transfiguration" : data["Transfiguration"]
    }
    feat4 = {
        "set" : data["Hogwarts House"],
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        #"Defense Against the Dark Arts": data["Defense Against the Dark Arts"],
        #"Potions" : data["Potions"],
        #"Charms" : data["Charms"],
        #"Divination" : data["Divination"],
        "Ancient Runes" : data["Ancient Runes"],
        #"Charms" : data["Charms"],
        #"Flying" : data["Flying"]
        #"Transfiguration" : data["Transfiguration"]
        #"Care of Magical Creatures" : data["Care of Magical Creatures"],
        #"Muggle Studies" : data["Muggle Studies"]

    }
    
    feature1 = check_nan(feat1)
    feature2 = check_nan(feat2)
    feature3 = check_nan(feat3)
    feature4 = check_nan(feat4)
    j = 0
    i = 1000
    while j != 1:
        j = rLogistic_train(feature1, "Ravenclaw")
        if i == j or round(i, 4) == round(j, 4):
            j = 1
        i = j
    j = 0
    i = 1000
    while  j != 1:
        j = rLogistic_train(feature2, "Slytherin")
        if i == j or round(i, 4) == round(j, 4):
            j = 1
        i = j
    j = 0
    i = 1000
    while j != 1:
        j = rLogistic_train(feature3, "Gryffindor")
        if i == j or round(i, 4) == round(j, 4):
            j = 1
        i = j
    j = 0
    i = 1000
    while j != 1:
        j = rLogistic_train(feature4, "Hufflepuff")
        if i == j or round(i, 4) == round(j, 4):
            j = 1
        i = j

if __name__ == "__main__":
    main()