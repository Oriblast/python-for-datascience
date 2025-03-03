import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from describe import *

"""

    nb = une corrélation matricielle est un rapport de similitude entre 2 ou plusieurs élément 
    il permet de mettre en avant facilement les éléments similaire ce rapport est proche de 1 si 
    les deux élément comparer son identique proche de 0 si ils ont rien en commun et -1 si ils
    sont tres divergeant 

"""

DATA_PATH = "dataset_train.csv"
data = pd.read_csv(DATA_PATH)
num_data = check_number(data)

# Calculer la matrice de corrélation
corr_matrix = num_data.corr()

# Trouver la paire de caractéristiques les plus corrélées
corr_matrix_unstacked = corr_matrix.unstack()
corr_matrix_unstacked = corr_matrix_unstacked[corr_matrix_unstacked != 1]  # elimine les corrélation == 1 
corr_matrix_unstacked = corr_matrix_unstacked.abs().idxmax()  # Trouver les indices de la plus grande corrélation

# Extraire les noms des colonnes les plus corrélées
feature_x, feature_y = corr_matrix_unstacked

# Affichage du scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(x=data[feature_x], y=data[feature_y], alpha=0.5, edgecolor='black')
plt.xlabel(feature_x)
plt.ylabel(feature_y)
plt.title(f"Scatter Plot des caractéristiques les plus similaires : {feature_x} vs {feature_y}")
plt.show()
