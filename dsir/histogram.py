from describe import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def recovery_dfByStr(data, s1: str, s2: str):
    """s1 la colonne et s2 la valeurs """
    if s1 not in data.columns:
        print("Colonne non trouvée")
        return None

    # Filtrer les lignes où s1 == s2
    filtered_data = data.loc[data[s1] == s2].copy()
    filtered_data = filtered_data.reset_index(drop=True)  # Réinitialise l'index
    
    if not filtered_data.empty:
        return filtered_data
    else:
        print("Aucune correspondance trouvée")
        return None

def my_home(data, s1:str, s2:str,i:int):
    d_Ravenclaw = recovery_dfByStr(data, s1, s2)
    Ravenclaw = check_number(d_Ravenclaw)
    mean_raven = {i: std(Ravenclaw)}
    mean_raven = pd.DataFrame(mean_raven).T
    mean_raven = mean_raven.drop(columns = ["Index"])
    print(mean_raven)
    return mean_raven

def main():
    data = pd.read_csv("dataset_train.csv")
    houses_std = pd.concat([
        my_home(data, "Hogwarts House", "Ravenclaw", 0),
        my_home(data, "Hogwarts House", "Slytherin", 1),
        my_home(data, "Hogwarts House", "Gryffindor", 2),
        my_home(data, "Hogwarts House", "Hufflepuff", 3)])

    print(houses_std)  # Vérification du DataFrame final
    house = mean_data(houses_std.T)

    # Affichage de l'histogramme
    plt.figure(figsize=(10, 6))

    plt.bar("Ravenclaw", house[0], alpha=0.5, label='Ravenclaw', color='green', edgecolor='black')

    plt.bar("Slytherin", house[1], alpha=0.5, label='Slytherin', color='blue', edgecolor='black')
    plt.bar("Gryffindor", house[2], alpha=0.5, label='Gryffindor', color='yellow', edgecolor='black')

    plt.bar("Hufflepuff", house[3], alpha=0.5, label='Hufflepuff', color='red', edgecolor='black')


    # Ajouter des titres et des labels
    plt.title('Distribution des âges et des scores')
    plt.xlabel('House')
    plt.ylabel('ecart-type')
    plt.legend()

    # Afficher l'histogramme
    plt.show()

if __name__ == "__main__":
    main()