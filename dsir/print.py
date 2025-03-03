import describe
import pandas as pd

def recovery_dfByStr(data, s1: str, s2):
    """s1 la colonne et s2 la valeurs """
    re = data[data[s1] == s2]
    if re:
        return re
    else: 
        print("aucune correspondance trouver")
        return None

def main():
    data = pd.read_csv("dataset_train.csv")
    print("ta petite")
    print(f"{recovery_dfByStr(data, 'Ravenclaw')}")
    
    