import pandas as pd 
import os

def load(path: str) -> pd.DataFrame:
    """
    load csv file 
    """
    try:
        if not os.path.exists(path):
            raise AssertionError("The file doesnt exist")
        if not path.lower().endswith('.csv'):
            raise AssertionError("The file fromat is not .csv")
        data = pd.read_csv(path)
        print(f"loading data csv of dimention: {data.shape}")
        
        return data

    except Exception as e:
        print(f"erreur: {e}")
        return None