import pandas as pd
import numpy as np

def isNumber(s):
    if not np.isnan(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    return False

def count(data):
    c = 0
    for i in range(len(data)):
        if isNumber(data[i]):
            c += 1.0
    return c

def count_df(data):
    tab_count = {col: 0 for col in data.columns}
    for current in data.columns:
        tab_count[current] += count(data[current])
    return tab_count

def mean(data):
    tab_mean = 0
    for i in range(len(data)):
        if isNumber(data[i]):
            tab_mean += data[i]
    if (tab_mean > 0.0):
        tab_mean /= count(data)
        return round(tab_mean, 6)
    else:
        return float("nan")

def mean_data(data):
    return {colum: mean(data[colum]) for colum in data.columns}

def ecart(data) -> float:
    """calcule de l'ecart type"""
    ecart_type = 0.0
    for i in range(len(data)):
        if isNumber(data[i]):
            ecart_type += (data[i] - mean(data)) ** 2
    if ecart_type > 0.0:
        return round(((1 / (count(data) - 1)) * ecart_type) ** 0.5, 6)

def std(data):
    """calcule de l'ecart type"""
    return {col :ecart(data[col]) for col in data.columns}

def check_number(data):
    nbr = {col: 0 for col in data.columns}
    for col in data:
        for i in range(len(data)):
            if isNumber(data[col][i]):
                nbr[col] = data[col].copy()
                break
    return pd.DataFrame(nbr)

def min(data):
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] < data[j]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp


def min_min(data):
    return {col :ecart(data[col]) for col in data.columns}

    
    

data_f = pd.read_csv("data.csv")

data = check_number(data_f)

d = std(data)
c = data.std()

print(f"ecart = {d} \n {c}")
