import numpy as np
import time

# Création de données
size = 10_000_000
a = np.random.rand(size)
b = np.random.rand(size)

# Avec une boucle Python
start = time.time()
c_loop = [a[i] + b[i] for i in range(size)]  # Stockage explicite dans une liste
end = time.time()
print(f"Boucle Python: {end - start:.4f} sec \n {len(c_loop)}\n")

# Avec NumPy (vectorisation)
start = time.time()
c_numpy = np.add(a, b)  # Stockage explicite dans un tableau NumPy
end = time.time()
print(f"NumPy: {end - start:.4f} sec \n {len(c_numpy)}")
