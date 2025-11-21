import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
 
from pathlib import Path
from ls_file_in_dir import ls_of_file

def distribution(path):
        ls_element = ls_of_file(path)
        base_path = Path(path)
        x = []
        y = []
        if not ls_element:
                return
        for i in ls_element:
                x.append(i.split('/')[-1])
                y.append(len(ls_element[i])) 

        plt.bar(x, y)
        plt.title("distribution")
        plt.xlabel("type_img")
        plt.ylabel("img_nb")
        plt.xticks(rotation=45, ha="right") #ratation du texte pour  la lisebilité
        plt.tight_layout() #gestion auto de la mise en page
        plt.savefig("distribution.png")
        plt.show()
        plt.figure(figsize=(10, 10))
        plt.pie(y, labels=x, autopct='%1.1f%%') # autopct montre les pourcentages
        plt.title(f"Répartition des images par maladie\n({base_path.name})")
        plt.tight_layout()
        plt.savefig(f'diagramme_circulaire_{base_path.name}.png')
        plt.show()

                
