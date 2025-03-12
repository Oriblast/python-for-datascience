from describe import *
import numpy as np
import pandas as pd 
import os 
import math
import csv
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

def sigmoïde(feature, w, b):
    """sigmoide fonction to determine probability y"""
    z = [0.0] * len(feature)
    y2 = [0] * len(feature)
    for i in feature.columns:
        if i != s1:
            for j in range(len(feature)):
                z[j] = feature[i][j] * w[i][0]
                
    for i in range(len(z)):
        z[i] += b 
    for i in range(len(y2)):
        y2[i] = 1 / (1 + math.exp(-z[i]))
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
    print(ll)
    return ll

def maj_b(b2, feature, y2, set_name):
    b = 0
    w = [0] * len(feature)
    """il s'agit de la dérivé de j sur w et b"""
    for i in range(len(feature)):
        if (feature["set"][i] == set_name):
            y = 1
        else:
            y = 0
        b += y2[i] - y
    b = b2.iloc[0, 0] - b2.iloc[0, 1] * ((1/len(feature)) * b)
    make_data2(["b", "a"], [b, 0.03], set_name)

def maj_w(w2, feature, y2, set_name, a):
    w = w2.copy()
    """il s'agit de la dérivé de j sur w et b"""
    for j in feature.columns:
        if j != "set":
            w.loc[0,j] = 0
            for i in range(len(feature)):
                if (feature["set"][i] == set_name):
                    y = 1
                else:
                    y = 0
                w.loc[0, j] += (y2[i] - y) * feature[j][i]
    for i in w2.columns:
        w2.loc[0, i] = w2.loc[0, i] - a * ((1/len(feature)) * w[i][0])
    make_data1(columnsName_ls(w2), columns_ls(w2), set_name)

def rLogistic_train(feature, set_name):
    """entrainement donné """
    if not os.path.exists(set_name + "_biais.csv") or not os.path.exists(set_name + "_featureW.csv"):
        make_data2(["b", "a"], [0, 1], set_name)
        ls = columnsName_ls(feature)
        ls.pop(0)
        init_data = [0.0] * len(ls)
        make_data1(ls, init_data, set_name)
    data_b = pd.read_csv(set_name + "_biais.csv")
    data_w = pd.read_csv(set_name + "_featureW.csv")
    y2 = sigmoïde(feature, data_w, data_b.iloc[0, 0])
    j = log_loss(feature, set_name, y2)
    if j > 0.3:
        print("dark")
        maj_b(data_b, feature, y2, set_name)
        maj_w(data_w, feature, y2, set_name, data_b["a"][0])
        return 0
    else:
        return 1
    return 0

def check_nan(data):
    feature = pd.DataFrame(data)
    for i in feature.columns:
        if i != s1:
            check_nb_str(data[i])
    return feature

def main ():
    """initialisation"""
    if not os.path.exists("dataset_train.csv"):
        print("fichier d'entrainement inexistant. File : dataset_train.csv")
        return
    data = pd.read_csv("dataset_train.csv")
    feat1 = {
        "set" : data["Hogwarts House"],
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Muggle Studies" : data["Muggle Studies"],
        "Charms" : data["Charms"],
        "Ancient Runes" : data["Ancient Runes"]
    }
    feat2 = {
        "set" : data["Hogwarts House"],
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Divination" : data["Divination"],
        "Ancient Runes" : data["Ancient Runes"]
    }
    feat3 = {
        "set" : data["Hogwarts House"],
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "History of Magic" : data["History of Magic"],
        "Flying" : data["Flying"],
        "Ancient Runes" : data["Ancient Runes"]
    }
    feat4 = {
        "set" : data["Hogwarts House"],
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Charms" : data["Charms"],
        "Ancient Runes" : data["Ancient Runes"]
    }
    
    feature1 = check_nan(feat1)
    feature2 = check_nan(feat2)
    feature3 = check_nan(feat3)
    feature4 = check_nan(feat4)

    j = 0
    while j == 0:
        j += rLogistic_train(feature1, "Ravenclaw")
    j = 0
    while j == 0:
        j +=rLogistic_train(feature2, "Slytherin")
    j = 0
    while j == 0:
        j += rLogistic_train(feature3, "Gryffindor")
    j = 0
    while j == 0:
        j += rLogistic_train(feature4, "Hufflepuff")

if __name__ == "__main__":
    main()