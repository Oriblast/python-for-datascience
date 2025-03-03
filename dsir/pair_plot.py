import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from describe import *

# Charger les données
DATA_PATH = "dataset_train.csv"
data = pd.read_csv(DATA_PATH)

# Sélectionner uniquement les colonnes numériques
num_data = check_number(data)

# Ajouter la maison comme catégorie pour la couleur
num_data["Hogwarts House"] = data["Hogwarts House"]
num_data = num_data.drop(columns = ["Index"])


# Affichage du Pair Plot
sns.pairplot(num_data, hue="Hogwarts House", diag_kind="hist")
plt.show()

num_data = check_number(num_data)

# Trouver les caractéristiques les moins corrélées
corr_matrix = num_data.corr()
corr_matrix_unstacked = corr_matrix.unstack()
corr_matrix_unstacked = corr_matrix_unstacked[corr_matrix_unstacked != 1]  # Exclure la diagonale
least_correlated = corr_matrix_unstacked.abs().idxmin()  # Indices de la plus petite corrélation

print(f"Les caractéristiques les plus différentes sont : {least_correlated}")
