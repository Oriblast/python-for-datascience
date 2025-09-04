import os 
import glob
def ls_of_file(dir):
        ls_dir = []
        ls_file = {}
        ls_dir = glob.glob(os.path.join(dir, '*'))
        for i in ls_dir:
            if os.path.isdir(i):
                ls_file[i] = glob.glob((os.path.join(i, '*'))
        ls_file = glob.glob(modele)
        return ls_file
