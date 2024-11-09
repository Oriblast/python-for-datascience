# aff_life.py
import matplotlib.pyplot as plt
from load_csv import load

def afficher_esperance_vie_pays(dataset, pays):
    # Filtrer les données pour le pays spécifié
    data_pays = dataset[dataset['country'] == pays]
    
    if data_pays.empty:
        print(f"Erreur : Aucune donnée trouvée pour le pays {pays}.")
        return
    
    # Extraire les années (colonnes après 'country')
    annees = data_pays.columns[1:]  # Sauter la colonne 'country'
    
    # Extraire les valeurs d'espérance de vie pour le pays
    esperance_vie = data_pays.values[0][1:]  # Sauter 'country' pour les valeurs
    
    # Créer un graphique
   # Créer un graphique
    plt.figure(figsize=(12, 6))  # Ajuster la taille du graphique
    plt.plot(annees, esperance_vie)

    # Ajouter un titre et des légendes aux axes
    plt.title(f"Évolution de l'espérance de vie - {pays}")
    plt.xlabel("Année")
    plt.ylabel("Espérance de vie")

    # Ajuster l'affichage des labels de l'axe X
    plt.xticks(rotation=45)  # Rotation et alignement des labels
    plt.tight_layout()  # Ajuster les marges pour éviter les chevauchements
    
    # Réduire le nombre de labels affichés sur l'axe X
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))

    # Afficher le graphique
    plt.show()

def main():
    # Charger le jeu de données à partir du fichier CSV
    dataset = load("life_expectancy_years.csv")
    
    if dataset is not None:
        # Afficher l'espérance de vie pour la France (ou un autre pays de votre campus)
        afficher_esperance_vie_pays(dataset, "France")
if __name__ == "__main__":
    main()
