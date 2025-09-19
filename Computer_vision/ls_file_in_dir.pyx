import os 
import glob


def ls_of_file(dir):
        ls_dir = []
        ls_file = {}
        ls_ = {}
        ls_dir = glob.glob(os.path.join(dir, '*'))
        for i in ls_dir:
                ii = os.path.abspath(i)
                if os.path.isdir(ii):
                        ls_file[ii] = [os.path.abspath(p) for p in glob.glob(os.path.join(ii, '*'))]
                else:
                        ls_file[ii] = []           
        return ls_file

