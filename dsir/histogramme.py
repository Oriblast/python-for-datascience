import pandas as pd
import matplotlib.pyplot as plt

# Exemple de DataFrame avec plusieurs colonnes
data = {'Nom': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'Âge': [22, 25, 35, 29, 31],
        'Score': [88, 92, 80, 85, 90]}

df = pd.DataFrame(data)

# Créer une figure
plt.figure(figsize=(10, 6))

# Graphique à barres pour la colonne 'Âge'
plt.bar(df['Nom'], df['Âge'], alpha=0.5, label='Âge', color='green', edgecolor='black')

# Graphique à barres pour la colonne 'Score'
plt.bar(df['Nom'], df['Score'], alpha=0.5, label='Score', color='blue', edgecolor='black')

# Ajouter des titres et des labels
plt.title('Âge et Score des participants')
plt.xlabel('Nom')
plt.ylabel('Valeur')
plt.legend()

# Afficher le graphique
plt.show()
