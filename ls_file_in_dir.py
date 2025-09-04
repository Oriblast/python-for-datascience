import os 
import glob
import matplotlib.pyplot as plt

def ls_of_file(dir):
        ls_dir = []
        ls_file = {}
        ls_dir = glob.glob(os.path.join(dir, '*'))
        for i in ls_dir:
            if os.path.isdir(i):
                ls_file[i] = glob.glob((os.path.join(i, '*'))
        ls_file = glob.glob(modele)
        return ls_file

def main():
        if not sys.argv:
                return -1
        ls_element = ls_of_file(sys.argv[0])
        x = []
        y = []
        for i in ls_element:
                x.append(i.split('/')[-1]))
                y.append(len(ls_element[i])) 

        plt.bar(x, y)
        plt.title("distribution")
        plt.xlabel("type_img")
        plt.ylabel("img_nb")
        plt.xticks(rotation=45, ha="rigth") #ratation du texte pour  la lisebilité 
        plt.tight_layout() #gestion auto de la mise en page 
        plt.savefig("distribution.png")
        plt.show()

        plt.figure(figsize=(10, 10))
        plt.pie(y, labels=x, autopct='%1.1f%%') # autopct montre les pourcentages
        plt.title(f"Répartition des images par maladie\n({base_path.name})")
        plt.tight_layout()
        plt.savefig(f'diagramme_circulaire_{base_path.name}.png')
        plt.show()
        
        
                
