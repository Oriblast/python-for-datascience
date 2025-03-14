from describe import *
import numpy as np
import pandas as pd 
import os 
import math
import csv
import sys
from sklearn.metrics import accuracy_score
from logreg_train import *

def deduction(yr, ys, yg, yh):
    if yr > ys and yr > yg and yr > yh:
        print("ravenclay")
        print(f"rave = {yr}\n")
        print(f"slytherin = {ys}\n")
        print(f"gryffindor = {yg}\n")
        print(f"hufflepuff = {yh}\n")
        return 1
    if ys > yr and ys > yg and ys > yh:
        print("serpent")
        print(f"rave = {yr}\n")
        print(f"slytherin = {ys}\n")
        print(f"gryffindor = {yg}\n")
        print(f"hufflepuff = {yh}\n")
        return 2     
    if yg > ys and yg > yr and yg > yh:
        print("grifon\n")
        print(f"rave = {yr}\n")
        print(f"slytherin = {ys}\n")
        print(f"gryffindor = {yg}\n")
        print(f"hufflepuff = {yh}\n")
        return 3 
    if yh > ys and yh > yg and yh > yr:
        print("pousoufre\n")
        print(f"rave = {yr}\n")
        print(f"slytherin = {ys}\n")
        print(f"gryffindor = {yg}\n")
        print(f"hufflepuff = {yh}\n")
        return 4
    return 4

def check_nan(data):
    feature = pd.DataFrame(data)
    for i in feature.columns:
        if i != s1:
            check_nb_str(feature[i])
    return feature

def main():
    """programme de prédiction"""
    if (len(sys.argv) != 2):
        print("pas d'arguments")
        return
    data = pd.read_csv(sys.argv[1])

    c_biais = pd.read_csv("Ravenclaw_biais.csv")
    c_feat = pd.read_csv("Ravenclaw_featureW.csv")
    s_biais = pd.read_csv("Slytherin_biais.csv")
    s_feat = pd.read_csv("Slytherin_featureW.csv")
    g_biais = pd.read_csv("Gryffindor_biais.csv")
    g_feat = pd.read_csv("Gryffindor_featureW.csv")
    h_biais = pd.read_csv("Hufflepuff_biais.csv")
    h_feat = pd.read_csv("Hufflepuff_featureW.csv")

    h = 0
    for i in data.columns:
        if i == "Astronomy" or h == 1:
            h = 0
            moyenne = data[i].mean()
            for j in range(len(data)):
                if np.isnan(data[i][j]):
                    data.loc[j, i] = moyenne
    
    for i in data.columns:
        if i == "Astronomy" or i == "Care of Magical Creatures" or i == "Ancient Runes" or i == "Herbology" or i == "Muggle Studies" or i == "Divination" or i == "Flying" or i == "Charms" or i == "Defense Against the Dark Arts" or i == "Transfiguration" or i == "Potions":
        #if i != "Hogwarts House":
            #check_nb_str(data[i])
            for j in range(len(data)):
                data.loc[j, i] /= 100

    feat1 = {
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Muggle Studies" : data["Muggle Studies"]
       # "Ancient Runes" : data["Ancient Runes"]
    }
    feat2 = {
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
        #"Astronomy": data["Astronomy"],
        #"Herbology": data["Herbology"],
        "History of Magic" : data["History of Magic"],
        "Flying" : data["Flying"]
        #"Ancient Runes" : data["Ancient Runes"]
        #"Transfiguration" : data["Transfiguration"]
    }
    feat4 = {
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
       # "Charms" : data["Charms"],
        #"Ancient Runes" : data["Ancient Runes"]
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

    }

    feature1 = check_nan(feat1)
    feature2 = check_nan(feat2)
    feature3 = check_nan(feat3)
    feature4 = check_nan(feat4)

    yr = sigmoïde(feature1, c_feat, c_biais.iloc[0, 0])
    ys = sigmoïde(feature2, s_feat, s_biais.iloc[0, 0])
    yg = sigmoïde(feature3, g_feat, g_biais.iloc[0, 0])
    yh = sigmoïde(feature4, h_feat, h_biais.iloc[0, 0])

    ls = [0] * len(feature1)
    with open("house.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Index","Hogwarts House"])
        for i in range(len(feature1)):
            print(f"rave = {yr[i]}\n")
            print(f"slytherin = {ys[i]}\n")
            print(f"gryffindor = {yg[i]}\n")
            print(f"hufflepuff = {yh[i]}\n")
            var = deduction(yr[i], ys[i], yg[i], yh[i])
            if var == 1:
                writer.writerow([i, "Ravenclaw"])
                ls[i] = "Ravenclaw"
            elif var == 2:
                writer.writerow([i, "Slytherin"])
                ls[i] = "Slytherin"
            elif var == 3:
                writer.writerow([i, "Gryffindor"])
                ls[i] = "Gryffindor"
            elif var == 4:
                writer.writerow([i, "Hufflepuff"])
                ls[i] = "Hufflepuff"
    """ls_r = data["Hogwarts House"].tolist()
    accuracy = accuracy_score(ls_r, ls)
    print(f'Accuracy du modèle : {accuracy:.2f}')
    print(ls_r)
    print(ls)"""


if __name__ == "__main__":
    main()