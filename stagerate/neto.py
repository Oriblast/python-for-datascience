import pandas as pd
from pyxlsb import open_workbook

def load_and_clean_data(file_path):
    # Lecture du fichier .xlsb
    with open_workbook(file_path) as wb:
        with wb.get_sheet(1) as sheet:
            data = [row for row in sheet.rows()]

    # Conversion en DataFrame
    columns = [item.v for item in data[0]]
    rows = [[item.v for item in row] for row in data[1:]]
    df = pd.DataFrame(rows, columns=columns)

    # Afficher les noms des colonnes
    print("Colonnes du DataFrame :")
    print(df.columns)

    # Nettoyage des données
    df['Date de commande'] = pd.to_datetime(df['Date de commande'], errors='coerce')
    df = df.dropna(subset=['Cod_cmd', 'Libellé produit', 'Vendeur', 'Univers', 'Nature', 'Date de commande', 'Montant cmd', 'Quantité', 'Prix transport', 'Délai transport annoncé'])  # Utilisez le nom correct de la colonne
    df['Montant cmd'] = pd.to_numeric(df['Montant cmd'], errors='coerce')
    df['Quantité'] = pd.to_numeric(df['Quantité'], errors='coerce')
    df['Prix transport'] = pd.to_numeric(df['Prix transport'], errors='coerce')
    df['Délai transport annoncé'] = pd.to_numeric(df['Délai transport annoncé'], errors='coerce')  # Utilisez le nom correct de la colonne
    
    # Sauvegarde des données nettoyées
    df.to_csv('cleaned_data.csv', index=False)

    return df

if __name__ == "__main__":
    file_path = '/home/kali/Documents/python/20210614 Ecommerce sales.xlsb'
    load_and_clean_data(file_path)
