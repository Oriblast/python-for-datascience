import pandas as pd
import re

# Charger les données nettoyées
df = pd.read_csv('cleaned_data.csv')

# Liste de couleurs prédéfinies
colors = ['blanc', 'noir', 'rouge', 'bleu', 'vert', 'jaune', 'rose', 'marron', 'gris', 'orange', 'violet', 'beige']

def extract_dimensions(description):
    # Regex pour les dimensions (e.g., 140x190 cm, 200x200, 50*50)
    dimensions = re.findall(r'\d{2,4}[\sx\*]\d{2,4}', description)
    return dimensions[0] if dimensions else None

def extract_color(description, colors):
    for color in colors:
        if color in description.lower():
            return color
    return None

# Ajouter les colonnes pour les dimensions et les couleurs
df['Dimensions'] = df['Libellé produit'].apply(extract_dimensions)
df['Color'] = df['Libellé produit'].apply(lambda x: extract_color(x, colors))

# Afficher les résultats
print(df[['Libellé produit', 'Dimensions', 'Color']])

# Enregistrer les données avec les nouvelles colonnes
df.to_csv('extracted_data.csv', index=False)
