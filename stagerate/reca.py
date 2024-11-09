import pandas as pd
import difflib

# Charger les données nettoyées
df = pd.read_csv('cleaned_data.csv')

# Extraire les catégories de nature existantes
categories = df['Nature'].unique().tolist()

def recategorize_product(description, categories):
    # Trouver la meilleure correspondance
    best_match = difflib.get_close_matches(description, categories, n=1, cutoff=0.6)
    # Retourner la meilleure correspondance si trouvée, sinon None
    return best_match[0] if best_match else None

# Ajouter une colonne pour les nouvelles catégories
df['New Nature'] = df['Libellé produit'].apply(lambda x: recategorize_product(x, categories))

# Afficher les lignes où la catégorie a été changée
changed_df = df[df['Nature'] != df['New Nature']]
print(changed_df[['Libellé produit', 'Nature', 'New Nature']])

# Enregistrer les modifications
df.to_csv('recategorized_data.csv', index=False)
