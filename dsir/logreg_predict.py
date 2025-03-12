from describe import *
import numpy as np
import pandas as pd 
import os 
import math
import csv
from logreg_train import *

def deduction(yr, ys, yg, yh):
    if yr > ys and yr > yg and yr > yh:
        return 1
    elif ys > yr and ys > yg and ys > yh:
        return 2     
    elif yg > ys and yg > yr and yg > yh:
        return 3 
    elif yh > ys and yh > yg and yh > yr:
        return 4
    return 0

def check_nan(data):
    feature = pd.DataFrame(data)
    for i in feature.columns:
        if i != s1:
            check_nb_str(data[i])
    return feature

def main():
    """programme de prédiction"""
    data = pd.read_csv("dataset_test.csv")
    c_biais = pd.read_csv("Ravenclaw_biais.csv")
    c_feat = pd.read_csv("Ravenclaw_featureW.csv")
    s_biais = pd.read_csv("Slytherin_biais.csv")
    s_feat = pd.read_csv("Slytherin_featureW.csv")
    g_biais = pd.read_csv("Gryffindor_biais.csv")
    g_feat = pd.read_csv("Gryffindor_featureW.csv")
    g_biais = pd.read_csv("Hufflepuff_biais.csv")
    g_feat = pd.read_csv("Hufflepuff_featureW.csv")

    feat1 = {
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Muggle Studies" : data["Muggle Studies"],
        "Charms" : data["Charms"],
        "Ancient Runes" : data["Ancient Runes"]
    }
    feat2 = {
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Divination" : data["Divination"],
        "Ancient Runes" : data["Ancient Runes"]
    }
    feat3 = {
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "History of Magic" : data["History of Magic"],
        "Flying" : data["Flying"],
        "Ancient Runes" : data["Ancient Runes"]
    }
    feat4 = {
        "Astronomy": data["Astronomy"],
        "Herbology": data["Herbology"],
        "Charms" : data["Charms"],
        "Ancient Runes" : data["Ancient Runes"]
    }

    feature1 = check_nan(feat1)
    feature2 = check_nan(feat2)
    feature3 = check_nan(feat3)
    feature4 = check_nan(feat4)

    yr = sigmoide(feature, c_feat, c_biais.iloc[0, 0])
    ys = sigmoide(feature, s_feat, s_biais.iloc[0, 0])
    yg = sigmoide(feature, g_feat, g_biais.iloc[0, 0])
    yh = sigmoide(feature, h_feat, h_biais.iloc[0, 0])

    with open("house.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Index","Hogwarts House"])
        for i in range(len(feature)):
            var = deduction(yr[i], ys[i], yg[i], yh[i])
            if var == 1:
                writer.writerow([i, "Ravenclaw"])
            elif var == 2:
                writer.writerow([i, "Slytherin"])
            elif var == 3:
                writer.writerow([i, "Gryffindor"])
            elif var == 4:
                writer.writerow([i, "Hufflepuff"])


if __name__ == "__main__":
    main()