import pandas as pd
import numpy as np
import sys

pd.options.mode.chained_assignment = None
def isNumber(s):
    """Vérifie si s est un nombre valide."""
    try:
        return not np.isnan(float(s))
    except ValueError:
        return False

def check_str(data):
    for i in range(len(data)):
        if (isinstance(data[i], str)):
            return False
    return True

def count(data):
    c = 0
    for i in range(len(data)):
        if isNumber(data.iloc[i]):
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
        if isNumber(data.iloc[i]):
            tab_mean += data.iloc[i]
    if count(data) > 0:
        return round(tab_mean / count(data), 6)

def mean_data(data):
    return {colum: mean(data[colum]) for colum in data.columns}

def ecart(data) -> float:
    """calcule de l'ecart type"""
    
    ecart_type = 0.0
    for i in range(len(data)):
        if isNumber(data.iloc[i]):
            ecart_type += (data.iloc[i] - mean(data)) ** 2
    if ecart_type > 0.0:
        return ((1 / (count(data) - 1)) * ecart_type) ** 0.5

def std(data):
    """calcule de l'ecart type"""
    return {col :ecart(data[col]) for col in data.columns}

def check_nb_str(data):
    count_nbr = 0
    count_str = 0
    count_void = 0
    for i in range(len(data)):
        if isNumber(data[i]):
            count_nbr += 1
        elif not data[i] or pd.isna(data[i]):
            count_void += 1
        else:
            count_str += 1
    if (count_nbr >= count_str or count_nbr - count_str > 0):
        for i in range(len(data)):
            if not isNumber(data[i]) and count_void - count_nbr - count_str < 0:
                data[i] = 0
        return True
    elif (count_void > 0 and count_void - count_str - count_nbr > 0):
        for i in range(len(data)):
            if i == 0:
                data[i] = 0.0
            else:
                data[i] = np.nan
        return True
    else:
        return False

def check_number(data):
    """Supprime les colonnes non numériques."""
    nbr = pd.DataFrame()
    for col in data:
        for i in range(len(data)):
            if check_nb_str(data[col]):
                nbr[col] = data[col].copy()
                break
            else :
                break
    return (nbr)

def min(data):
    data = data.values.copy()  # Convertir en NumPy pour éviter SettingWithCopyWarning
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] < data[j]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
    return data[0]


def min_min(data):
    return {col :min(data[col]) for col in data.columns}


def max(data):
    data = data.values.copy()
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] > data[j]:
                temp = data[i].copy()
                data[i] = data[j].copy()
                data[j] = temp
    return data[0]


def max_max(data):
    return {col :max(data[col]) for col in data.columns}

def percen(data, p):
    data = sorted(data)
    index = (p / 100) * (len(data) - 1)
    index_int = int(index)
    fraction = index - index_int

    if index_int >= len(data) - 1:  # Si p = 100, retourne la dernière valeur
        return data[-1]
    
    # Si l'index est un entier, pas besoin d'interpolation
    if fraction == 0:
        return data[index_int]
    
    # Interpolation linéaire
    return data[index_int] + fraction * (data[index_int + 1] - data[index_int])


def percen0(data, perce):
    return {col :percen(data[col], perce) for col in data.columns}

def describe_statistics(data):
    """Calcule les statistiques et les retourne sous forme de DataFrame"""
    stats = {
        "Count": count_df(data),
        "Mean": mean_data(data),
        "Std": std(data),
        "Min": min_min(data),
        "25%": percen0(data, 25),
        "50%": percen0(data, 50),
        "75%": percen0(data, 75),
        "Max": max_max(data),
    }
    stats = pd.DataFrame(stats)  # Convertit en DataFrame Pandas
    return stats.T

def main():
    """affichage des statistique csv"""
    if (len(sys.argv) != 2):
        print("pas d'arguments")
        return
    data = pd.read_csv(sys.argv[1])
    data_nbr = check_number(data)
    print(f"{data_nbr}\n\n")
    print(f"{describe_statistics(data_nbr)}\n\n")
    print(f"\n\n{data.describe()}")

if __name__ == "__main__":
    main()
